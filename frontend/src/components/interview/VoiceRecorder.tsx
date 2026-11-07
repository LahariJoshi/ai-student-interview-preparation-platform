"use client";

import React, { useState, useRef, useEffect } from "react";
import { Mic, Square, Loader2, Volume2, Sparkles, RefreshCw } from "lucide-react";
import { getApiBaseUrl } from "@/lib/api";
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

      const hostUrl = getApiBaseUrl();
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
    <div className="bg-[#F8FAFC] border border-[#E5E9EF] rounded-2xl p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Volume2 className="w-4 h-4 text-[#F5A623]" />
          <span className="text-xs font-semibold text-[#202B38]">
            Voice Answer Mode
          </span>
          <span className="text-[10px] text-[#8993A0] bg-white border border-[#E5E9EF] px-2 py-0.5 rounded-full font-medium">
            AI Speech Analysis
          </span>
        </div>

        {isRecording && (
          <div className="flex items-center gap-2 text-rose-600 text-xs font-mono font-bold animate-pulse bg-rose-50 px-2.5 py-1 rounded-full border border-rose-200">
            <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping" />
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
            className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-slate-50 text-[#123E63] border border-[#E5E9EF] rounded-xl text-xs font-semibold transition shadow-sm disabled:opacity-50"
          >
            <Mic className="w-3.5 h-3.5 text-[#F5A623]" />
            <span>Record Voice Answer</span>
          </button>
        ) : (
          <button
            type="button"
            onClick={stopRecording}
            className="flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-xs font-semibold transition shadow-sm"
          >
            <Square className="w-3.5 h-3.5 fill-current" />
            <span>Stop & Process Speech</span>
          </button>
        )}

        {isProcessing && (
          <div className="flex items-center gap-2 text-xs text-[#123E63]">
            <Loader2 className="w-3.5 h-3.5 animate-spin text-[#F5A623]" />
            <span className="font-medium">Analyzing delivery metrics...</span>
          </div>
        )}
      </div>

      {/* Live speech preview */}
      {isRecording && liveTranscript && (
        <div className="text-xs text-[#202B38] italic bg-white p-3 rounded-xl border border-[#E5E9EF]">
          <span className="text-[#123E63] font-semibold not-italic">Live Hearing: </span>
          "{liveTranscript}"
        </div>
      )}

      {errorMsg && (
        <div className="text-xs text-rose-600 bg-rose-50 p-2.5 rounded-xl border border-rose-200">
          {errorMsg}
        </div>
      )}
    </div>
  );
}