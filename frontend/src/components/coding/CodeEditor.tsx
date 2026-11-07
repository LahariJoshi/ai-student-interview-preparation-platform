"use client";

import React, { useState, useEffect, useRef } from "react";
import { ProgrammingLanguage } from "@/types/coding";
import {
  Play,
  Send,
  RotateCcw,
  Code,
  Terminal,
  Keyboard,
  Check,
  AlertCircle,
} from "lucide-react";

interface CodeEditorProps {
  questionId: string;
  starterCodeMap?: Record<string, string>;
  onRunCode: (language: string, code: string) => Promise<void>;
  onSubmitCode: (language: string, code: string) => Promise<void>;
  isRunning?: boolean;
  isSubmitting?: boolean;
  activeLanguage?: string;
  onLanguageChange?: (language: string) => void;
}

interface LanguageOption {
  value: ProgrammingLanguage;
  label: string;
  defaultCode: string;
  supported: boolean;
}

const SUPPORTED_LANGUAGES: LanguageOption[] = [
  {
    value: "python",
    label: "Python 3",
    defaultCode: `def solve():\n    # Write your solution here\n    pass\n\nif __name__ == '__main__':\n    import sys\n    input_data = sys.stdin.read().strip()\n    # Process input and print result\n`,
    supported: true,
  },
  {
    value: "javascript",
    label: "JavaScript (Node.js)",
    defaultCode: `function solve(input) {\n  // Write your solution here\n}\n\nlet input = '';\nprocess.stdin.setEncoding('utf-8');\nprocess.stdin.on('data', (chunk) => {\n  input += chunk;\n});\nprocess.stdin.on('end', () => {\n  solve(input.trim());\n});\n`,
    supported: true,
  },
  {
    value: "typescript",
    label: "TypeScript",
    defaultCode: `function solve(input: string): void {\n  // Write your solution here\n}\n`,
    supported: true,
  },
  {
    value: "java",
    label: "Java 17",
    defaultCode: `import java.util.*;\nimport java.io.*;\n\npublic class Solution {\n    public static void main(String[] args) throws Exception {\n        Scanner scanner = new Scanner(System.in);\n        // Read input and print answer\n    }\n}\n`,
    supported: true,
  },
  {
    value: "cpp",
    label: "C++ (GCC)",
    defaultCode: `#include <iostream>\n#include <vector>\n#include <string>\n\nusing namespace std;\n\nint main() {\n    ios_base::sync_with_stdio(false);\n    cin.tie(NULL);\n    // Read input and print output\n    return 0;\n}\n`,
    supported: true,
  },
];

export default function CodeEditor({
  questionId,
  starterCodeMap = {},
  onRunCode,
  onSubmitCode,
  isRunning = false,
  isSubmitting = false,
  activeLanguage: controlledLanguage,
  onLanguageChange,
}: CodeEditorProps) {
  const [selectedLanguage, setSelectedLanguage] = useState<string>(() => {
    if (
      controlledLanguage &&
      SUPPORTED_LANGUAGES.some((l) => l.value === controlledLanguage && l.supported)
    ) {
      return controlledLanguage;
    }
    return "python";
  });
  const [code, setCode] = useState<string>("");
  const [lineCount, setLineCount] = useState<number>(1);
  const containerRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null);
  const lastTriggerRef = useRef<number>(0);

  const codeRef = useRef(code);
  const langRef = useRef(selectedLanguage);
  const isRunningRef = useRef(isRunning);
  const isSubmittingRef = useRef(isSubmitting);
  const onRunCodeRef = useRef(onRunCode);
  const onSubmitCodeRef = useRef(onSubmitCode);

  useEffect(() => {
    codeRef.current = code;
  }, [code]);
  useEffect(() => {
    langRef.current = selectedLanguage;
  }, [selectedLanguage]);
  useEffect(() => {
    isRunningRef.current = isRunning;
  }, [isRunning]);
  useEffect(() => {
    isSubmittingRef.current = isSubmitting;
  }, [isSubmitting]);
  useEffect(() => {
    onRunCodeRef.current = onRunCode;
  }, [onRunCode]);
  useEffect(() => {
    onSubmitCodeRef.current = onSubmitCode;
  }, [onSubmitCode]);

  useEffect(() => {
    if (
      controlledLanguage &&
      controlledLanguage !== selectedLanguage &&
      SUPPORTED_LANGUAGES.some((l) => l.value === controlledLanguage && l.supported)
    ) {
      setSelectedLanguage(controlledLanguage);
    }
  }, [controlledLanguage, selectedLanguage]);

  useEffect(() => {
    const starter = starterCodeMap[selectedLanguage];
    if (starter && starter.trim()) {
      setCode(starter);
    } else {
      const fallback = SUPPORTED_LANGUAGES.find((l) => l.value === selectedLanguage)?.defaultCode || "";
      setCode(fallback);
    }
  }, [questionId, selectedLanguage, starterCodeMap]);

  useEffect(() => {
    const lines = (code.match(/\n/g) || []).length + 1;
    setLineCount(Math.max(lines, 1));
  }, [code]);

  const handleScroll = () => {
    if (textareaRef.current && lineNumbersRef.current) {
      lineNumbersRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  };

  const triggerRun = () => {
    const now = Date.now();
    if (now - lastTriggerRef.current < 300) return;
    lastTriggerRef.current = now;

    const currentCode = codeRef.current;
    const currentLang = langRef.current;
    if (!currentCode.trim()) return;

    if (onRunCodeRef.current) {
      onRunCodeRef.current(currentLang, currentCode);
    }
  };

  const triggerSubmit = () => {
    const now = Date.now();
    if (now - lastTriggerRef.current < 300) return;
    lastTriggerRef.current = now;

    const currentCode = codeRef.current;
    const currentLang = langRef.current;
    if (!currentCode.trim()) return;

    if (onSubmitCodeRef.current) {
      onSubmitCodeRef.current(currentLang, currentCode);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Tab") {
      e.preventDefault();
      const target = e.currentTarget;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      const spaces = "    ";
      const newCode = code.substring(0, start) + spaces + code.substring(end);
      setCode(newCode);
      requestAnimationFrame(() => {
        target.selectionStart = target.selectionEnd = start + spaces.length;
      });
      return;
    }

    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      if (e.shiftKey) {
        if (!isSubmittingRef.current && !isRunningRef.current) {
          triggerSubmit();
        }
      } else {
        if (!isRunningRef.current && !isSubmittingRef.current) {
          triggerRun();
        }
      }
    }
  };

  const handleLanguageChange = (newLang: string) => {
    if (newLang === selectedLanguage) return;
    if (code.trim().length > 30) {
      const confirmed = window.confirm(
        "Changing language will reset editor to the new language template. Are you sure you want to proceed?"
      );
      if (!confirmed) return;
    }

    setSelectedLanguage(newLang);
    if (onLanguageChange) {
      onLanguageChange(newLang);
    }
  };

  const handleResetCode = () => {
    const confirmed = window.confirm("Reset code back to the initial starter template?");
    if (!confirmed) return;

    const starter = starterCodeMap[selectedLanguage];
    if (starter && starter.trim()) {
      setCode(starter);
    } else {
      const fallback = SUPPORTED_LANGUAGES.find((l) => l.value === selectedLanguage)?.defaultCode || "";
      setCode(fallback);
    }
  };

  return (
    <div
      ref={containerRef}
      className="bg-white rounded-2xl shadow-card border border-[#E5E9EF] flex flex-col h-full overflow-hidden"
    >
      {/* Editor Top Toolbar */}
      <div className="px-4 py-2.5 bg-[#F8F9FA] border-b border-[#E5E9EF] flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Code className="w-4 h-4 text-[#123E63]" />
            <select
              value={selectedLanguage}
              onChange={(e) => handleLanguageChange(e.target.value)}
              disabled={isRunning || isSubmitting}
              className="bg-white border border-[#E5E9EF] rounded-lg px-2.5 py-1 text-xs text-[#202B38] font-semibold focus:outline-none focus:border-[#123E63]"
            >
              {SUPPORTED_LANGUAGES.map((lang) => (
                <option key={lang.value} value={lang.value} disabled={!lang.supported}>
                  {lang.label}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={handleResetCode}
            disabled={isRunning || isSubmitting}
            title="Reset to starter code"
            className="inline-flex items-center gap-1 text-[#8993A0] hover:text-[#202B38] px-2 py-1 rounded transition text-xs font-semibold"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset</span>
          </button>
        </div>

        {/* Shortcuts Indicator */}
        <div className="hidden sm:flex items-center gap-3 text-[11px] text-[#8993A0]">
          <span className="inline-flex items-center gap-1">
            <kbd className="px-1.5 py-0.5 rounded bg-white border border-[#E5E9EF] font-mono text-[10px]">
              Ctrl+Enter
            </kbd>
            <span>Run</span>
          </span>
          <span className="inline-flex items-center gap-1">
            <kbd className="px-1.5 py-0.5 rounded bg-white border border-[#E5E9EF] font-mono text-[10px]">
              Ctrl+Shift+Enter
            </kbd>
            <span>Submit</span>
          </span>
        </div>
      </div>

      {/* Code Editor Surface */}
      <div
        onClick={() => textareaRef.current?.focus()}
        className="relative flex-1 min-h-[380px] bg-[#0A1A2A] flex overflow-hidden font-mono text-xs cursor-text"
      >
        {/* Line Numbers Gutter */}
        <div
          ref={lineNumbersRef}
          aria-hidden="true"
          className="w-12 bg-[#06121D] border-r border-[#122B42] py-3 text-right pr-3 select-none text-[#4A6882] font-mono text-xs overflow-hidden leading-6"
        >
          {Array.from({ length: lineCount }).map((_, idx) => (
            <div key={idx + 1} className="h-6">
              {idx + 1}
            </div>
          ))}
        </div>

        {/* Textarea Code Input */}
        <textarea
          ref={textareaRef}
          value={code}
          onChange={(e) => setCode(e.target.value)}
          onKeyDown={handleKeyDown}
          onScroll={handleScroll}
          spellCheck={false}
          autoCapitalize="off"
          autoComplete="off"
          autoCorrect="off"
          placeholder="// Write your solution here..."
          className="flex-1 bg-transparent text-[#E1EAF5] p-3 outline-none resize-none font-mono text-xs leading-6 selection:bg-[#123E63]/80 overflow-y-auto whitespace-pre tab-4"
        />
      </div>

      {/* Editor Bottom Bar */}
      <div className="px-4 py-3 bg-[#F8F9FA] border-t border-[#E5E9EF] flex items-center justify-between gap-3">
        <div className="text-[11px] text-[#8993A0] flex items-center gap-2 font-medium">
          <span>{lineCount} lines</span>
          <span>&bull;</span>
          <span>{code.length} characters</span>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => triggerRun()}
            disabled={isRunning || isSubmitting || !code.trim()}
            className="inline-flex items-center gap-1.5 px-4 py-2 bg-white hover:bg-slate-50 text-[#123E63] border border-[#E5E9EF] rounded-xl text-xs font-bold transition shadow-xs disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 text-[#123E63] ${isRunning ? "animate-spin" : ""}`} />
            <span>{isRunning ? "Running..." : "Run Code"}</span>
          </button>

          <button
            onClick={() => triggerSubmit()}
            disabled={isRunning || isSubmitting || !code.trim()}
            className="inline-flex items-center gap-1.5 px-5 py-2 bg-[#F5A623] hover:bg-[#E09212] text-white rounded-xl text-xs font-bold transition shadow-sm disabled:opacity-50"
          >
            <Send className={`w-3.5 h-3.5 ${isSubmitting ? "animate-bounce" : ""}`} />
            <span>{isSubmitting ? "Evaluating..." : "Submit Solution"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
