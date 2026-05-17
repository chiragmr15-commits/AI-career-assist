import React from 'react';
import { motion } from 'framer-motion';
import { interviewService } from '../services/api';

export const InterviewSimulator = () => {
  const [step, setStep] = React.useState(1);
  const [session, setSession] = React.useState(null);
  const [currentQuestionIdx, setCurrentQuestionIdx] = React.useState(0);
  const [answers, setAnswers] = React.useState({});
  const [loading, setLoading] = React.useState(false);

  const [config, setConfig] = React.useState({
    interview_type: 'Mixed',
    job_role: '',
    difficulty: 'Medium',
    num_questions: 5,
  });

  const handleStartInterview = async () => {
    setLoading(true);
    try {
      const response = await interviewService.generateInterview(config);
      setSession(response.data);
      setStep(2);
    } catch (error) {
      console.error('Failed to start interview:', error);
    }
    setLoading(false);
  };

  const handleAnswerSubmit = async (answer) => {
    if (!session?.questions?.[currentQuestionIdx]) return;
    const questionId = session.questions[currentQuestionIdx].id;
    
    try {
      setAnswers(prev => ({ ...prev, [questionId]: answer }));
      if (currentQuestionIdx < session.questions.length - 1) {
        setCurrentQuestionIdx(prev => prev + 1);
      } else {
        // Complete interview
        await interviewService.completeInterview(session.id);
        setStep(3);
      }
    } catch (error) {
      console.error('Failed to submit answer:', error);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold gradient-text">Interview Simulator</h1>

      {step === 1 ? (
        <InterviewSetup
          config={config}
          setConfig={setConfig}
          onStart={handleStartInterview}
          loading={loading}
        />
      ) : step === 2 ? (
        <InterviewQuestion
          session={session}
          currentQuestionIdx={currentQuestionIdx}
          onAnswerSubmit={handleAnswerSubmit}
          totalQuestions={session?.questions?.length || 0}
        />
      ) : (
        <InterviewComplete session={session} onBack={() => setStep(1)} />
      )}
    </div>
  );
};

const InterviewSetup = ({ config, setConfig, onStart, loading }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="card space-y-4"
  >
    <div>
      <label className="block text-sm font-medium mb-2">Interview Type</label>
      <select
        value={config.interview_type}
        onChange={(e) => setConfig(prev => ({ ...prev, interview_type: e.target.value }))}
        className="input"
      >
        <option>Technical</option>
        <option>HR</option>
        <option>Mixed</option>
      </select>
    </div>

    <div>
      <label className="block text-sm font-medium mb-2">Job Role (Optional)</label>
      <input
        type="text"
        value={config.job_role}
        onChange={(e) => setConfig(prev => ({ ...prev, job_role: e.target.value }))}
        placeholder="e.g., Software Engineer"
        className="input"
      />
    </div>

    <div>
      <label className="block text-sm font-medium mb-2">Difficulty</label>
      <select
        value={config.difficulty}
        onChange={(e) => setConfig(prev => ({ ...prev, difficulty: e.target.value }))}
        className="input"
      >
        <option>Easy</option>
        <option>Medium</option>
        <option>Hard</option>
      </select>
    </div>

    <div>
      <label className="block text-sm font-medium mb-2">Number of Questions: {config.num_questions}</label>
      <input
        type="range"
        min="3"
        max="10"
        value={config.num_questions}
        onChange={(e) => setConfig(prev => ({ ...prev, num_questions: parseInt(e.target.value) }))}
        className="w-full"
      />
    </div>

    <button
      onClick={onStart}
      disabled={loading}
      className="w-full btn btn-primary disabled:opacity-50"
    >
      {loading ? 'Starting...' : 'Start Interview'}
    </button>
  </motion.div>
);

const InterviewQuestion = ({ session, currentQuestionIdx, onAnswerSubmit, totalQuestions }) => {
  const [answer, setAnswer] = React.useState('');
  const question = session?.questions?.[currentQuestionIdx];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Progress */}
      <div className="card">
        <div className="flex justify-between items-center mb-2">
          <span>Question {currentQuestionIdx + 1} of {totalQuestions}</span>
          <span className="text-primary-400">{Math.round((currentQuestionIdx + 1) / totalQuestions * 100)}%</span>
        </div>
        <div className="h-2 bg-dark-700 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${(currentQuestionIdx + 1) / totalQuestions * 100}%` }}
            transition={{ duration: 0.5 }}
            className="h-full bg-gradient-to-r from-primary-500 to-blue-600"
          />
        </div>
      </div>

      {/* Question */}
      <div className="card">
        <div className="flex items-start gap-4">
          <div className="text-3xl">🎤</div>
          <div>
            <div className="text-sm text-gray-400 mb-2">{question?.category}</div>
            <h3 className="text-xl font-bold">{question?.question_text}</h3>
            {question?.difficulty_level && (
              <div className="mt-3 inline-block px-3 py-1 bg-dark-700 rounded text-sm">
                Difficulty: {question.difficulty_level}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Answer Input */}
      <div className="card">
        <label className="block text-sm font-medium mb-2">Your Answer</label>
        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type your answer here..."
          className="w-full px-4 py-3 bg-dark-800 border border-dark-600 rounded-lg text-gray-100 placeholder-gray-500 focus:outline-none focus:border-primary-500 resize-none h-40"
        />
      </div>

      <button
        onClick={() => onAnswerSubmit(answer)}
        disabled={!answer.trim()}
        className="w-full btn btn-primary disabled:opacity-50"
      >
        {currentQuestionIdx === totalQuestions - 1 ? 'Complete Interview' : 'Next Question'}
      </button>
    </motion.div>
  );
};

const InterviewComplete = ({ session, onBack }) => (
  <motion.div
    initial={{ opacity: 0, scale: 0.9 }}
    animate={{ opacity: 1, scale: 1 }}
    className="space-y-6"
  >
    <div className="card text-center">
      <div className="text-6xl mb-4">🎉</div>
      <h2 className="text-3xl font-bold gradient-text mb-2">Interview Complete!</h2>
      <p className="text-gray-400">Great job! Check your results below.</p>
    </div>

    <div className="card">
      <h3 className="text-2xl font-bold mb-4">Your Score</h3>
      <div className="text-5xl font-bold text-primary-400 text-center">
        {session?.overall_score?.toFixed(0) || 0}%
      </div>
    </div>

    <button onClick={onBack} className="w-full btn btn-primary">
      Start New Interview
    </button>
  </motion.div>
);
