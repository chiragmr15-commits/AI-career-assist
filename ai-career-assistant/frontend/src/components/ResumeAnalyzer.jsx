import React from 'react';
import { motion } from 'framer-motion';
import { resumeService } from '../services/api';

export const ResumeAnalyzer = () => {
  const [file, setFile] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [result, setResult] = React.useState(null);
  const [dragActive, setDragActive] = React.useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === 'dragenter' || e.type === 'dragover');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files?.[0]) {
      setFile(e.dataTransfer.files[0]);
    }
    setDragActive(false);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const response = await resumeService.upload(file);
      setResult(response.data);
    } catch (error) {
      console.error('Upload failed:', error);
    }
    setLoading(false);
  };

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await resumeService.analyze();
      setResult(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold gradient-text">Resume Analyzer</h1>

      {!result ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Upload Area */}
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`card border-2 border-dashed ${dragActive ? 'border-primary-400 bg-primary-400/10' : 'border-dark-600'} cursor-pointer transition-colors p-12 text-center`}
          >
            <div className="text-5xl mb-3">📄</div>
            <h3 className="text-xl font-bold mb-2">
              {file ? file.name : 'Drop your resume here'}
            </h3>
            <p className="text-gray-400 mb-4">or click to select</p>
            <input
              type="file"
              accept=".pdf,.docx,.doc"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="hidden"
              id="file-input"
            />
            <label htmlFor="file-input" className="btn btn-primary cursor-pointer">
              Choose File
            </label>
          </div>

          {file && (
            <motion.button
              onClick={handleUpload}
              disabled={loading}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="w-full btn btn-primary disabled:opacity-50"
            >
              {loading ? 'Uploading...' : 'Upload & Analyze'}
            </motion.button>
          )}

          {/* Or analyze existing */}
          <div className="relative flex items-center">
            <div className="flex-1 border-t border-dark-600"></div>
            <span className="px-4 text-gray-400">OR</span>
            <div className="flex-1 border-t border-dark-600"></div>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full btn btn-secondary disabled:opacity-50"
          >
            Analyze Existing Resume
          </button>
        </motion.div>
      ) : (
        <ResultsView result={result} onBack={() => setResult(null)} />
      )}
    </div>
  );
};

const ResultsView = ({ result, onBack }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="space-y-6"
  >
    <button onClick={onBack} className="btn btn-secondary">
      ← Back
    </button>

    {/* ATS Score */}
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-2xl font-bold">ATS Score</h3>
        <div className="text-5xl font-bold text-primary-400">{result.ats_score?.toFixed(0) || 0}%</div>
      </div>
      <div className="h-3 bg-dark-700 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${result.ats_score || 0}%` }}
          transition={{ duration: 1 }}
          className="h-full bg-gradient-to-r from-primary-500 to-blue-600"
        />
      </div>
    </div>

    {/* Skills */}
    <div className="card">
      <h3 className="text-xl font-bold mb-4">Identified Skills ({result.skills?.length || 0})</h3>
      <div className="flex flex-wrap gap-2">
        {result.skills?.map((skill, i) => (
          <motion.span
            key={i}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.05 }}
            className="px-3 py-1 bg-primary-500/20 text-primary-300 rounded-full text-sm"
          >
            {skill}
          </motion.span>
        ))}
      </div>
    </div>

    {/* Suggestions */}
    <div className="card">
      <h3 className="text-xl font-bold mb-4">Suggestions</h3>
      <ul className="space-y-2">
        {result.suggestions?.map((suggestion, i) => (
          <motion.li
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
            className="flex items-start gap-3"
          >
            <span className="text-green-400 mt-1">✓</span>
            <span>{suggestion}</span>
          </motion.li>
        ))}
      </ul>
    </div>
  </motion.div>
);
