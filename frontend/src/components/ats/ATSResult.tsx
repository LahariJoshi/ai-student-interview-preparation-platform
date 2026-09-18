"use client";

interface ATSResultProps {
  result: {
    ats_score: number;
    formatting_score: number;
    keyword_match_score: number;
    semantic_similarity_score: number;
    action_impact_score: number;
    matched_skills: string[];
    missing_skills: string[];
    analysis_status: string;
  };
}

export default function ATSResult({ result }: ATSResultProps) {
  return (
    <div className="space-y-6">

      {/* ATS Score */}
      <div className="glass-card p-8 text-center">
        <p className="text-slate-400 text-sm uppercase tracking-wider">
          ATS Compatibility Score
        </p>

        <div className="mt-4">
          <span className="text-6xl font-extrabold text-white">
            {result.ats_score}
          </span>

          <span className="text-slate-400 text-xl">
            {" "}/ 100
          </span>
        </div>

        <p className="mt-3 text-emerald-400 text-sm">
          Analysis completed successfully
        </p>
      </div>

      {/* Score Breakdown */}
      <div>
        <h2 className="text-xl font-bold text-white mb-4">
          Score Breakdown
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <div className="glass-card p-5">
            <p className="text-slate-400 text-sm">
              Formatting
            </p>

            <p className="text-2xl font-bold text-white mt-2">
              {result.formatting_score}
            </p>
          </div>

          <div className="glass-card p-5">
            <p className="text-slate-400 text-sm">
              Keyword Match
            </p>

            <p className="text-2xl font-bold text-white mt-2">
              {result.keyword_match_score}
            </p>
          </div>

          <div className="glass-card p-5">
            <p className="text-slate-400 text-sm">
              Semantic Similarity
            </p>

            <p className="text-2xl font-bold text-white mt-2">
              {result.semantic_similarity_score}
            </p>
          </div>

          <div className="glass-card p-5">
            <p className="text-slate-400 text-sm">
              Action & Impact
            </p>

            <p className="text-2xl font-bold text-white mt-2">
              {result.action_impact_score}
            </p>
          </div>

        </div>
      </div>

      {/* Skills */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Matched Skills */}
        <div className="glass-card p-6">
          <h2 className="text-lg font-bold text-white">
            Matched Skills
          </h2>

          {result.matched_skills.length > 0 ? (
            <div className="flex flex-wrap gap-2 mt-4">
              {result.matched_skills.map((skill) => (
                <span
                  key={skill}
                  className="px-3 py-1 rounded-full bg-emerald-900/40 border border-emerald-700 text-emerald-300 text-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-slate-400 text-sm mt-4">
              No matching skills detected.
            </p>
          )}
        </div>

        {/* Missing Skills */}
        <div className="glass-card p-6">
          <h2 className="text-lg font-bold text-white">
            Missing Skills
          </h2>

          {result.missing_skills.length > 0 ? (
            <div className="flex flex-wrap gap-2 mt-4">
              {result.missing_skills.map((skill) => (
                <span
                  key={skill}
                  className="px-3 py-1 rounded-full bg-red-900/40 border border-red-700 text-red-300 text-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-emerald-400 text-sm mt-4">
              No missing skills detected.
            </p>
          )}
        </div>

      </div>

      {/* Improvement Message */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-bold text-white">
          Improvement Areas
        </h2>

        <ul className="mt-4 space-y-2 text-slate-400 text-sm">

          {result.keyword_match_score < 60 && (
            <li>
              • Improve keyword alignment between your resume and
              the target job description.
            </li>
          )}

          {result.semantic_similarity_score < 60 && (
            <li>
              • Add more relevant experience, projects, and skills
              related to the target role.
            </li>
          )}

          {result.formatting_score < 70 && (
            <li>
              • Improve resume formatting and section structure
              for ATS readability.
            </li>
          )}

          {result.action_impact_score < 60 && (
            <li>
              • Strengthen achievement descriptions using action
              verbs and measurable results.
            </li>
          )}

          {result.keyword_match_score >= 60 &&
            result.semantic_similarity_score >= 60 &&
            result.formatting_score >= 70 &&
            result.action_impact_score >= 60 && (
              <li className="text-emerald-400">
                • Your resume shows good alignment with this job
                description.
              </li>
            )}

        </ul>
      </div>

    </div>
  );
}