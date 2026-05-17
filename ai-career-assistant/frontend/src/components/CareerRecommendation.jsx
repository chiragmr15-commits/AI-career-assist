import React from 'react';
import { motion } from 'framer-motion';
import { careerService } from '../services/api';

export const CareerRecommendation = () => {
  const [step, setStep] = React.useState(1);
  const [interests, setInterests] = React.useState([]);
  const [recommendations, setRecommendations] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const careerOptions = [
    'Software Engineer',
    'Data Analyst',
    'AI/ML Engineer',
    'UI/UX Designer',
    'DevOps Engineer',
    'Product Manager',
    'Business Analyst',
    'Cloud Architect',
  ];

  const toggleInterest = (career) => {
    setInterests(prev =>
      prev.includes(career)
        ? prev.filter(c => c !== career)
        : [...prev, career]
    );
  };

  const handleGetRecommendation = async () => {
    setLoading(true);
    try {
      const response = await careerService.getRecommendation(interests);
      setRecommendations(response.data);
      setStep(2);
    } catch (error) {
      console.error('Failed to get recommendations:', error);
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold gradient-text">Career Recommendation</h1>

      {step === 1 ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="card">
            <h3 className="text-xl font-bold mb-6">Select your interests</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {careerOptions.map((career, i) => (
                <motion.button
                  key={i}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => toggleInterest(career)}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    interests.includes(career)
                      ? 'border-primary-500 bg-primary-500/20 text-primary-300'
                      : 'border-dark-600 hover:border-dark-500'
                  }`}
                >
                  {career}
                </motion.button>
              ))}
            </div>
          </div>

          <button
            onClick={handleGetRecommendation}
            disabled={loading || interests.length === 0}
            className="w-full btn btn-primary disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Get Recommendations'}
          </button>
        </motion.div>
      ) : (
        <RecommendationsView recommendations={recommendations} onBack={() => setStep(1)} />
      )}
    </div>
  );
};

const RecommendationsView = ({ recommendations, onBack }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="space-y-6"
  >
    <button onClick={onBack} className="btn btn-secondary">
      ← Back
    </button>

    {/* Reasoning */}
    <div className="card">
      <h3 className="text-2xl font-bold mb-2 gradient-text">Your Recommendation</h3>
      <p className="text-gray-300">{recommendations.reasoning}</p>
    </div>

    {/* Recommended Careers */}
    <div className="card">
      <h3 className="text-xl font-bold mb-4">Recommended Careers</h3>
      <div className="space-y-3">
        {recommendations.recommended_careers?.map((career, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
            className="p-4 bg-primary-500/10 border border-primary-500/30 rounded-lg"
          >
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-bold text-primary-300">{career}</h4>
                <p className="text-sm text-gray-400">Career Path</p>
              </div>
              <span className="text-2xl">💼</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>

    {/* Skills to Learn */}
    <div className="card">
      <h3 className="text-xl font-bold mb-4">Skills to Learn</h3>
      <div className="flex flex-wrap gap-2">
        {recommendations.recommended_skills?.map((skill, i) => (
          <motion.span
            key={i}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.05 }}
            className="px-3 py-1 bg-amber-500/20 text-amber-300 rounded-full text-sm"
          >
            📚 {skill}
          </motion.span>
        ))}
      </div>
    </div>

    {/* Career Readiness */}
    <div className="card">
      <h3 className="text-xl font-bold mb-4">Career Readiness</h3>
      <div className="text-5xl font-bold text-primary-400 mb-3">
        {recommendations.confidence_score?.toFixed(0) || 0}%
      </div>
      <div className="h-3 bg-dark-700 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${(recommendations.confidence_score || 0) * 100}%` }}
          transition={{ duration: 1 }}
          className="h-full bg-gradient-to-r from-primary-500 to-blue-600"
        />
      </div>
    </div>
  </motion.div>
);
