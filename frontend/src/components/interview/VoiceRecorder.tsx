"use client";

import React, { useState, useRef, useEffect } from "react";
import { Mic, Square, Loader2, Volume2, Sparkles, RefreshCw } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { AudioUploadResponse } from "@/types/interview";

interface VoiceRecorderProps {
  sessionId: string;
  onTranscriptReady: (transcript: string, metrics: any, duration: number) => void;
  disabled?: boolean;
}

export default function VoiceRecorder({
  sessionId,
  onTranscriptReady,
  disabled = false,
}: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordDuration, setRecordDuration] = useState(0);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [liveTranscript, setLiveTranscript] = useState<string>("");

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const recognitionRef = useRef<any>(null);

  // Initialize Web Speech API if supported
  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onresult = (event: any) => {
          let currentText = "";
          for (let i = 0; i < event.results.length; i++) {
            currentText += event.results[i][0].transcript + " ";
          }
          setLiveTranscript(currentText.trim());
        };

        recognition.onerror = (e: any) => {
          console.warn("Speech recognition warning:", e.error);
        };

        recognitionRef.current = recognition;
      }
    }

    return () => {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch {}
      }
    };
  }, []);

  const startRecording = async () => {
    setErrorMsg(null);
    setLiveTranscript("");
    setRecordDuration(0);
    audioChunksRef.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        // Stop all audio tracks to release microphone
        stream.getTracks().forEach((track) => track.stop());
        await processRecordedAudio();
      };

      mediaRecorder.start(250); // Slice chunks every 250ms
      setIsRecording(true);

      // Start duration counter
      const startTimestamp = Date.now();
      timerIntervalRef.current = setInterval(() => {
        setRecordDuration(Math.floor((Date.now() - startTimestamp) / 1000));
      }, 1000);

      // Start Web Speech recognition if supported
      if (recognitionRef.current) {
        try {
          recognitionRef.current.start();
        } catch {}
      }
    } catch (err: any) {
      setErrorMsg(
        err.name === "NotAllowedError"
          ? "Microphone access was denied. Please allow microphone permissions in your browser."
          : "Unable to access microphone device."
      );
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
      }
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch {}
      }
    }
  };

  const processRecordedAudio = async () => {
    setIsProcessing(true);
    try {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("audio_file", audioBlob, "answer.webm");
      formData.append("duration_seconds", recordDuration.toString());
      formData.append("transcription_text", liveTranscript);

      const hostUrl =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      const res = await fetch(
        `${hostUrl}/interviews/sessions/${sessionId}/audio-upload`,
        {
          method: "POST",
          body: formData,
          credentials: "include",
        }
      );

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Audio upload and analysis failed.");
      }

      const data: AudioUploadResponse = await res.json();
      onTranscriptReady(data.transcript, data.delivery_metrics, data.duration_seconds);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to process audio.");
      // Fallback: if browser captured live transcript, still supply it to the user
      if (liveTranscript) {
        onTranscriptReady(liveTranscript, {}, recordDuration);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Volume2 className="w-4 h-4 text-sky-400" />
          <span className="text-sm font-semibold text-slate-200">
            Voice Answer Mode
          </span>
          <span className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">
            Optional
          </span>
        </div>

        {isRecording && (
          <div className="flex items-center gap-2 text-rose-400 text-xs font-mono font-bold animate-pulse">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping" />
            REC {formatTimer(recordDuration)}
          </div>
        )}
      </div>

      <div className="flex items-center gap-3">
        {!isRecording ? (
          <button
            type="button"
            onClick={startRecording}
            disabled={disabled || isProcessing}
            className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700 rounded-lg text-sm font-medium transition disabled:opacity-50"
          >
            <Mic className="w-4 h-4" />
            <span>Record Voice Answer</span>
          </button>
        ) : (
          <button
            type="button"
            onClick={stopRecording}
            className="flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-sm font-medium transition shadow-lg shadow-rose-950"
          >
            <Square className="w-4 h-4 fill-current" />
            <span>Stop & Process Speech</span>
          </button>
        )}

        {isProcessing && (
          <div className="flex items-center gap-2 text-xs text-sky-400">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Analyzing delivery metrics...</span>
          </div>
        )}
      </div>

      {/* Live speech preview if available */}
      {isRecording && liveTranscript && (
        <div className="text-xs text-slate-400 italic bg-slate-950/60 p-2.5 rounded border border-slate-800/80">
          <span className="text-sky-400 font-semibold not-italic">Live Hearing: </span>
          "{liveTranscript}"
        </div>
      )}

      {errorMsg && (
        <div className="text-xs text-rose-400 bg-rose-950/40 p-2 rounded border border-rose-800/60">
          {errorMsg}
        </div>
      )}
    </div>
  );
}
