"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import {
  Mic,
  Square,
  Play,
  Pause,
  RotateCcw,
  Trash2,
  Send,
  AlertCircle,
  Volume2,
  CheckCircle,
} from "lucide-react";
import RecordingStatus, { RecordingState, formatTime } from "./RecordingStatus";

export interface RecordedAudioData {
  blob: Blob;
  url: string;
  durationSeconds: number;
}

interface AudioRecorderProps {
  maxDurationSeconds?: number;
  onRecordingComplete?: (data: RecordedAudioData) => void;
  onSubmitRecording?: (data: RecordedAudioData) => void;
  onDeleteRecording?: () => void;
  isSubmitting?: boolean;
  className?: string;
}

export default function AudioRecorder({
  maxDurationSeconds = 300, // 5 minutes max
  onRecordingComplete,
  onSubmitRecording,
  onDeleteRecording,
  isSubmitting = false,
  className = "",
}: AudioRecorderProps) {
  // Recording State
  const [status, setStatus] = useState<RecordingState>("idle");
  const [duration, setDuration] = useState<number>(0);
  const [audioLevel, setAudioLevel] = useState<number>(0);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Playback State
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);

  // Media & Audio Context Refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const timerIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const audioElementRef = useRef<HTMLAudioElement | null>(null);

  // Clean up streams & audio context on unmount
  const cleanupStream = useCallback(() => {
    if (timerIntervalRef.current) {
      clearInterval(timerIntervalRef.current);
      timerIntervalRef.current = null;
    }
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    if (audioContextRef.current && audioContextRef.current.state !== "closed") {
      audioContextRef.current.close().catch(() => {});
      audioContextRef.current = null;
    }
  }, []);

  useEffect(() => {
    return () => {
      cleanupStream();
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [cleanupStream, audioUrl]);

  // Handle live volume meter
  const startAudioMeter = (stream: MediaStream) => {
    try {
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      if (!AudioCtx) return;

      const audioCtx = new AudioCtx();
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 64;
      const source = audioCtx.createMediaStreamSource(stream);
      source.connect(analyser);

      audioContextRef.current = audioCtx;
      analyserRef.current = analyser;

      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const updateMeter = () => {
        if (!analyserRef.current) return;
        analyserRef.current.getByteFrequencyData(dataArray);

        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
          sum += dataArray[i];
        }
        const avg = sum / bufferLength;
        const normalized = Math.min(100, Math.round((avg / 128) * 100));
        setAudioLevel(normalized);

        animationFrameRef.current = requestAnimationFrame(updateMeter);
      };

      updateMeter();
    } catch {
      // AudioContext fallback without crashing
    }
  };

  // Start Recording Handler
  const handleStartRecording = async () => {
    setErrorMessage(null);

    // 1. Check browser support
    if (typeof window === "undefined" || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setStatus("error");
      setErrorMessage("Audio recording is not supported in this browser. Please use a modern browser like Chrome, Firefox, or Edge.");
      return;
    }

    if (!window.MediaRecorder) {
      setStatus("error");
      setErrorMessage("MediaRecorder API is not available in this browser.");
      return;
    }

    try {
      setStatus("requesting");

      // 2. Request microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      streamRef.current = stream;

      // 3. Determine best supported audio mimeType
      let mimeType = "";
      const candidateTypes = [
        "audio/webm;codecs=opus",
        "audio/webm",
        "audio/mp4",
        "audio/ogg;codecs=opus",
        "audio/ogg",
      ];
      for (const type of candidateTypes) {
        if (MediaRecorder.isTypeSupported(type)) {
          mimeType = type;
          break;
        }
      }

      const options = mimeType ? { mimeType } : undefined;
      const mediaRecorder = new MediaRecorder(stream, options);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const chunks = audioChunksRef.current;
        const finalType = mediaRecorder.mimeType || "audio/webm";
        const blob = new Blob(chunks, { type: finalType });

        cleanupStream();

        // 4. Validate empty recording
        if (blob.size === 0 || duration < 1) {
          setStatus("error");
          setErrorMessage("Recording was empty or too brief. Please speak into your microphone and try again.");
          return;
        }

        const url = URL.createObjectURL(blob);
        setAudioBlob(blob);
        setAudioUrl(url);
        setStatus("recorded");

        if (onRecordingComplete) {
          onRecordingComplete({ blob, url, durationSeconds: duration });
        }
      };

      // 5. Start audio level visualizer
      startAudioMeter(stream);

      // 6. Start MediaRecorder
      mediaRecorder.start(250); // Emit chunk every 250ms
      setStatus("recording");
      setDuration(0);

      // 7. Start duration timer
      timerIntervalRef.current = setInterval(() => {
        setDuration((prev) => {
          if (prev >= maxDurationSeconds - 1) {
            handleStopRecording();
            return maxDurationSeconds;
          }
          return prev + 1;
        });
      }, 1000);
    } catch (err: any) {
      cleanupStream();
      setStatus("error");

      if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
        setErrorMessage(
          "Microphone permission was denied. Please allow microphone access in your browser site settings and try again."
        );
      } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
        setErrorMessage("No microphone input device detected. Please connect a working microphone.");
      } else if (err.name === "NotReadableError" || err.name === "TrackStartError") {
        setErrorMessage("Microphone is currently in use by another application.");
      } else {
        setErrorMessage(err.message || "Failed to initialize audio recording.");
      }
    }
  };

  // Stop Recording Handler
  const handleStopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
    }
  };

  // Delete & Reset Recording
  const handleDeleteRecording = () => {
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }
    setAudioBlob(null);
    setAudioUrl(null);
    setDuration(0);
    setCurrentTime(0);
    setIsPlaying(false);
    setStatus("idle");
    setErrorMessage(null);

    if (onDeleteRecording) {
      onDeleteRecording();
    }
  };

  // Re-record
  const handleRecordAgain = () => {
    handleDeleteRecording();
    setTimeout(() => {
      handleStartRecording();
    }, 150);
  };

  // Audio Playback Controls
  const togglePlayPause = () => {
    if (!audioElementRef.current || !audioUrl) return;

    if (isPlaying) {
      audioElementRef.current.pause();
      setIsPlaying(false);
    } else {
      audioElementRef.current
        .play()
        .then(() => setIsPlaying(true))
        .catch(() => setIsPlaying(false));
    }
  };

  const handleAudioTimeUpdate = () => {
    if (audioElementRef.current) {
      setCurrentTime(audioElementRef.current.currentTime);
    }
  };

  const handleAudioEnded = () => {
    setIsPlaying(false);
    setCurrentTime(0);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const targetTime = parseFloat(e.target.value);
    if (audioElementRef.current) {
      audioElementRef.current.currentTime = targetTime;
      setCurrentTime(targetTime);
    }
  };

  // Submit Answer with Audio
  const handleSubmit = () => {
    if (!audioBlob || !audioUrl || isSubmitting) return;

    if (onSubmitRecording) {
      onSubmitRecording({
        blob: audioBlob,
        url: audioUrl,
        durationSeconds: duration,
      });
    }
  };

  return (
    <div className={`w-full rounded-2xl bg-slate-900/80 border border-slate-800 p-6 space-y-6 ${className}`}>
      {/* Hidden audio element for preview */}
      {audioUrl && (
        <audio
          ref={audioElementRef}
          src={audioUrl}
          onTimeUpdate={handleAudioTimeUpdate}
          onEnded={handleAudioEnded}
          className="hidden"
        />
      )}

      {/* Recording Status and Waveform Indicator */}
      <RecordingStatus
        status={status}
        durationSeconds={status === "recorded" ? duration : duration}
        audioLevel={audioLevel}
        errorMessage={errorMessage}
      />

      {/* Primary Action Controls based on State */}
      <div className="flex flex-col items-center justify-center gap-4">
        {/* State 1: IDLE or ERROR */}
        {(status === "idle" || status === "error") && (
          <div className="flex flex-col items-center gap-3">
            <button
              type="button"
              onClick={handleStartRecording}
              className="flex items-center gap-2.5 px-6 py-3 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-semibold text-sm shadow-lg shadow-rose-950/40 transition active:scale-95 cursor-pointer"
            >
              <Mic className="w-5 h-5 text-white animate-pulse" />
              <span>Start Speaking & Recording</span>
            </button>
            <p className="text-xs text-slate-400">
              Click to grant microphone access and answer by voice. Max duration: {Math.floor(maxDurationSeconds / 60)} min.
            </p>
          </div>
        )}

        {/* State 2: REQUESTING PERMISSION */}
        {status === "requesting" && (
          <div className="flex items-center gap-3 py-2 text-sky-400 text-sm font-medium">
            <span className="w-4 h-4 border-2 border-sky-400 border-t-transparent rounded-full animate-spin" />
            <span>Waiting for microphone permission in your browser...</span>
          </div>
        )}

        {/* State 3: RECORDING IN PROGRESS */}
        {status === "recording" && (
          <div className="flex items-center gap-4">
            <button
              type="button"
              onClick={handleStopRecording}
              className="flex items-center gap-2.5 px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-rose-400 border border-rose-500/40 font-semibold text-sm shadow-md transition active:scale-95 cursor-pointer"
            >
              <Square className="w-4 h-4 fill-rose-500 text-rose-500" />
              <span>Stop & Preview Recording</span>
            </button>
          </div>
        )}

        {/* State 4: RECORDED - Preview & Actions */}
        {status === "recorded" && audioUrl && (
          <div className="w-full max-w-md space-y-4">
            {/* Playback Scrub Bar */}
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1.5 font-medium text-slate-300">
                  <Volume2 className="w-4 h-4 text-sky-400" />
                  Voice Answer Preview
                </span>
                <span className="font-mono">
                  {formatTime(Math.floor(currentTime))} / {formatTime(duration)}
                </span>
              </div>

              {/* Progress Bar / Range */}
              <input
                type="range"
                min="0"
                max={duration || 1}
                step="0.1"
                value={currentTime}
                onChange={handleSeek}
                className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-sky-400"
              />

              {/* Player Controls */}
              <div className="flex items-center justify-center gap-3 pt-1">
                <button
                  type="button"
                  onClick={togglePlayPause}
                  className="flex items-center justify-center w-10 h-10 rounded-full bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold transition shadow-md cursor-pointer"
                >
                  {isPlaying ? <Pause className="w-5 h-5 fill-current" /> : <Play className="w-5 h-5 fill-current ml-0.5" />}
                </button>
              </div>
            </div>

            {/* Action Buttons: Delete, Record Again, Submit */}
            <div className="flex items-center justify-between gap-3 pt-2">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={handleDeleteRecording}
                  disabled={isSubmitting}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800/80 hover:bg-rose-950/40 text-slate-400 hover:text-rose-400 text-xs font-semibold border border-slate-700 hover:border-rose-500/40 transition disabled:opacity-50 cursor-pointer"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>Discard</span>
                </button>

                <button
                  type="button"
                  onClick={handleRecordAgain}
                  disabled={isSubmitting}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition disabled:opacity-50 cursor-pointer"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Record Again</span>
                </button>
              </div>

              {onSubmitRecording && (
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                  className="flex items-center gap-2 px-5 py-2 rounded-xl bg-sky-500 hover:bg-sky-400 disabled:bg-sky-500/50 text-slate-950 text-xs font-bold shadow-md shadow-sky-500/20 transition active:scale-95 disabled:cursor-not-allowed cursor-pointer"
                >
                  {isSubmitting ? (
                    <>
                      <span className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                      <span>Submitting...</span>
                    </>
                  ) : (
                    <>
                      <Send className="w-3.5 h-3.5" />
                      <span>Submit Recording</span>
                    </>
                  )}
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
