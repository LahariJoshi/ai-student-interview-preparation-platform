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
    label: "TypeScript (Coming Soon)",
    defaultCode: `function solve(input: string): void {\n  // Write your solution here\n}\n`,
    supported: false,
  },
  {
    value: "java",
    label: "Java 17 (Coming Soon)",
    defaultCode: `import java.util.*;\nimport java.io.*;\n\npublic class Solution {\n    public static void main(String[] args) throws Exception {\n        Scanner scanner = new Scanner(System.in);\n        // Read input and print answer\n    }\n}\n`,
    supported: false,
  },
  {
    value: "cpp",
    label: "C++ (GCC) (Coming Soon)",
    defaultCode: `#include <iostream>\n#include <vector>\n#include <string>\n\nusing namespace std;\n\nint main() {\n    ios_base::sync_with_stdio(false);\n    cin.tie(NULL);\n    // Read input and print output\n    return 0;\n}\n`,
    supported: false,
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
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null);

  // Sync controlled language if changed from parent
  useEffect(() => {
    if (
      controlledLanguage &&
      controlledLanguage !== selectedLanguage &&
      SUPPORTED_LANGUAGES.some((l) => l.value === controlledLanguage && l.supported)
    ) {
      setSelectedLanguage(controlledLanguage);
    }
  }, [controlledLanguage, selectedLanguage]);

  // Load starter code on mount or when language / question changes
  useEffect(() => {
    const starter = starterCodeMap[selectedLanguage];
    if (starter && starter.trim()) {
      setCode(starter);
    } else {
      const fallback = SUPPORTED_LANGUAGES.find((l) => l.value === selectedLanguage)?.defaultCode || "";
      setCode(fallback);
    }
  }, [questionId, selectedLanguage, starterCodeMap]);

  // Update line count
  useEffect(() => {
    const lines = (code.match(/\n/g) || []).length + 1;
    setLineCount(Math.max(lines, 1));
  }, [code]);

  // Synchronize scroll between line numbers gutter and textarea
  const handleScroll = () => {
    if (textareaRef.current && lineNumbersRef.current) {
      lineNumbersRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  };

  // Handle Tab key indentation
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Run shortcut: Ctrl+Enter or Cmd+Enter
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!isRunning && !isSubmitting) {
        onRunCode(selectedLanguage, code);
      }
      return;
    }

    // Submit shortcut: Ctrl+Shift+Enter or Cmd+Shift+Enter
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter" && e.shiftKey) {
      e.preventDefault();
      if (!isRunning && !isSubmitting) {
        onSubmitCode(selectedLanguage, code);
      }
      return;
    }

    // Tab indentation
    if (e.key === "Tab") {
      e.preventDefault();
      const textarea = textareaRef.current;
      if (!textarea) return;

      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const tabSpaces = "  ";

      const newCode = code.substring(0, start) + tabSpaces + code.substring(end);
      setCode(newCode);

      // Restore cursor position after state updates
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + tabSpaces.length;
      }, 0);
    }
  };

  const handleLanguageChange = (newLang: string) => {
    const langOption = SUPPORTED_LANGUAGES.find((l) => l.value === newLang);
    if (!langOption || !langOption.supported) return;

    const isDirty = code !== (starterCodeMap[selectedLanguage] || "");
    if (isDirty) {
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
    <div className="glass-card flex flex-col h-full overflow-hidden border border-slate-800">
      {/* Editor Top Toolbar */}
      <div className="px-4 py-2.5 bg-slate-900/90 border-b border-slate-800 flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Code className="w-4 h-4 text-sky-400" />
            <select
              value={selectedLanguage}
              onChange={(e) => handleLanguageChange(e.target.value)}
              disabled={isRunning || isSubmitting}
              className="bg-slate-950 border border-slate-700 rounded-md px-2.5 py-1 text-xs text-white focus:outline-none focus:border-sky-500 font-medium"
            >
              {SUPPORTED_LANGUAGES.map((lang) => (
                <option
                  key={lang.value}
                  value={lang.value}
                  disabled={!lang.supported}
                  className={!lang.supported ? "text-slate-500 bg-slate-900" : "text-white bg-slate-950"}
                >
                  {lang.label}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={handleResetCode}
            disabled={isRunning || isSubmitting}
            title="Reset to starter code"
            className="inline-flex items-center gap-1 text-slate-400 hover:text-white px-2 py-1 rounded hover:bg-slate-800 transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset</span>
          </button>
        </div>

        {/* Shortcuts Indicator */}
        <div className="hidden md:flex items-center gap-3 text-[11px] text-slate-400">
          <span className="inline-flex items-center gap-1">
            <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 font-mono text-[10px]">
              Ctrl+Enter
            </kbd>
            <span>Run</span>
          </span>
          <span className="inline-flex items-center gap-1">
            <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 font-mono text-[10px]">
              Ctrl+Shift+Enter
            </kbd>
            <span>Submit</span>
          </span>
        </div>
      </div>

      {/* Editor Workspace with Line Numbers */}
      <div className="relative flex-1 min-h-[360px] bg-slate-950 flex overflow-hidden font-mono text-xs">
        {/* Line Numbers Gutter */}
        <div
          ref={lineNumbersRef}
          aria-hidden="true"
          className="w-12 bg-slate-900/60 border-r border-slate-800 py-3 text-right pr-3 select-none text-slate-600 font-mono text-xs overflow-hidden leading-6"
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
          className="flex-1 bg-transparent text-slate-100 p-3 outline-none resize-none font-mono text-xs leading-6 selection:bg-sky-500/30 overflow-y-auto whitespace-pre tab-4"
        />
      </div>

      {/* Editor Bottom Status & Action Bar */}
      <div className="px-4 py-3 bg-slate-900/90 border-t border-slate-800 flex items-center justify-between gap-3">
        <div className="text-[11px] text-slate-400 flex items-center gap-2">
          <span>{lineCount} lines</span>
          <span>•</span>
          <span>{code.length} characters</span>
        </div>

        <div className="flex items-center gap-3">
          {/* Run Button */}
          <button
            onClick={() => onRunCode(selectedLanguage, code)}
            disabled={isRunning || isSubmitting || !code.trim()}
            className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-semibold transition disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 text-sky-400 ${isRunning ? "animate-spin" : ""}`} />
            <span>{isRunning ? "Running..." : "Run Code"}</span>
          </button>

          {/* Submit Button */}
          <button
            onClick={() => onSubmitCode(selectedLanguage, code)}
            disabled={isRunning || isSubmitting || !code.trim()}
            className="inline-flex items-center gap-2 px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold transition shadow-sm disabled:opacity-50"
          >
            <Send className={`w-3.5 h-3.5 ${isSubmitting ? "animate-bounce" : ""}`} />
            <span>{isSubmitting ? "Evaluating..." : "Submit Solution"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
