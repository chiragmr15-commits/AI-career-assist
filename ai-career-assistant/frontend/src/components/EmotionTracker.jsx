import React from 'react';
import { motion } from 'framer-motion';
import { emotionService } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export const EmotionTracker = () => {
  const [tab, setTab] = React.useState('log');
  const [formData, setFormData] = React.useState({
    journal_entry: '',
    mood: 'Neutral',
    stress_level: 'Moderate',
    energy_level: 5,
  });
  const [history, setHistory] = React.useState([]);
  const [trend, setTrend] = React.useState(null);
  const [tips, setTips] = React.useState([]);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    if (tab === 'history') {
      fetchHistory();
    } else if (tab === 'trend') {
      fetchTrend();
    } else if (tab === 'tips') {
      fetchTips();
    }
  }, [tab]);

  const fetchHistory = async () => {
    try {
      const response = await emotionService.getHistory(30);
      setHistory(response.data);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  const fetchTrend = async () => {
    try {
      const response = await emotionService.getTrend();
      setTrend(response.data);
    } catch (error) {
      console.error('Failed to fetch trend:', error);
    }
  };

  const fetchTips = async () => {
    try {
      const response = await emotionService.getTips();
      setTips(response.data);
    } catch (error) {
      console.error('Failed to fetch tips:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await emotionService.addEntry(formData);
      setFormData({ journal_entry: '', mood: 'Neutral', stress_level: 'Moderate', energy_level: 5 });
      setTab('history');
    } catch (error) {
      console.error('Failed to log mood:', error);
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold gradient-text">Wellness Tracker</h1>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-dark-600">
        {['log', 'history', 'trend', 'tips'].map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 font-medium border-b-2 transition-colors ${
              tab === t
                ? 'border-primary-500 text-primary-400'
                : 'border-transparent text-gray-400 hover:text-gray-300'
            }`}
          >
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {/* Content */}
      {tab === 'log' && <LogMoodForm formData={formData} setFormData={setFormData} onSubmit={handleSubmit} loading={loading} />}
      {tab === 'history' && <MoodHistory history={history} />}
      {tab === 'trend' && <MoodTrend trend={trend} history={history} />}
      {tab === 'tips' && <MotivationalTips tips={tips} />}
    </div>
  );
};

const LogMoodForm = ({ formData, setFormData, onSubmit, loading }) => (
  <motion.form
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    onSubmit={onSubmit}
    className="card space-y-4"
  >
    <div>
      <label className="block text-sm font-medium mb-2">How are you feeling?</label>
      <textarea
        value={formData.journal_entry}
        onChange={(e) => setFormData(prev => ({ ...prev, journal_entry: e.target.value }))}
        placeholder="Share your thoughts and feelings..."
        className="w-full px-4 py-3 bg-dark-800 border border-dark-600 rounded-lg text-gray-100 placeholder-gray-500 focus:outline-none focus:border-primary-500 resize-none h-40"
        required
      />
    </div>

    <div className="grid grid-cols-2 gap-4">
      <div>
        <label className="block text-sm font-medium mb-2">Mood</label>
        <select
          value={formData.mood}
          onChange={(e) => setFormData(prev => ({ ...prev, mood: e.target.value }))}
          className="input"
        >
          <option>Very Happy</option>
          <option>Happy</option>
          <option>Neutral</option>
          <option>Sad</option>
          <option>Very Sad</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Stress Level</label>
        <select
          value={formData.stress_level}
          onChange={(e) => setFormData(prev => ({ ...prev, stress_level: e.target.value }))}
          className="input"
        >
          <option>Low</option>
          <option>Moderate</option>
          <option>High</option>
          <option>Very High</option>
        </select>
      </div>
    </div>

    <div>
      <label className="block text-sm font-medium mb-2">Energy Level: {formData.energy_level}/10</label>
      <input
        type="range"
        min="1"
        max="10"
        value={formData.energy_level}
        onChange={(e) => setFormData(prev => ({ ...prev, energy_level: parseInt(e.target.value) }))}
        className="w-full"
      />
    </div>

    <button type="submit" disabled={loading} className="w-full btn btn-primary disabled:opacity-50">
      {loading ? 'Saving...' : 'Save Entry'}
    </button>
  </motion.form>
);

const MoodHistory = ({ history }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="space-y-3"
  >
    {history.length === 0 ? (
      <div className="card text-center py-8 text-gray-400">
        No mood entries yet. Start by logging your mood!
      </div>
    ) : (
      history.map((entry, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.05 }}
          className="card"
        >
          <div className="flex items-start justify-between mb-2">
            <div>
              <div className="font-bold">{entry.mood}</div>
              <div className="text-sm text-gray-400">
                {new Date(entry.created_at).toLocaleDateString()}
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm">Energy: {entry.energy_level}/10</div>
              <div className="text-sm">Stress: {entry.stress_level}</div>
            </div>
          </div>
          <p className="text-gray-300 text-sm">{entry.journal_entry?.slice(0, 100)}...</p>
        </motion.div>
      ))
    )}
  </motion.div>
);

const MoodTrend = ({ trend, history }) => {
  const chartData = history.slice().reverse().map((entry, i) => ({
    date: new Date(entry.created_at).toLocaleDateString(),
    mood: entry.energy_level,
    stress: entry.stress_level === 'Low' ? 1 : entry.stress_level === 'Moderate' ? 2 : entry.stress_level === 'High' ? 3 : 4,
  }));

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {trend && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="card text-center">
            <div className="text-gray-400 text-sm">Avg Mood</div>
            <div className="text-3xl font-bold text-primary-400">{trend.weekly_average_mood?.toFixed(1) || 0}</div>
          </div>
          <div className="card text-center">
            <div className="text-gray-400 text-sm">Avg Stress</div>
            <div className="text-3xl font-bold text-amber-400">{trend.weekly_average_stress?.toFixed(1) || 0}</div>
          </div>
          <div className="card text-center">
            <div className="text-gray-400 text-sm">Avg Anxiety</div>
            <div className="text-3xl font-bold text-red-400">{trend.weekly_average_anxiety?.toFixed(1) || 0}</div>
          </div>
          <div className="card text-center">
            <div className="text-gray-400 text-sm">Avg Motivation</div>
            <div className="text-3xl font-bold text-green-400">{trend.weekly_average_motivation?.toFixed(1) || 0}</div>
          </div>
        </div>
      )}

      <div className="card">
        <h3 className="text-xl font-bold mb-4">Trend Chart</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
            <Legend />
            <Line type="monotone" dataKey="mood" stroke="#3b82f6" strokeWidth={2} />
            <Line type="monotone" dataKey="stress" stroke="#f59e0b" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
};

const MotivationalTips = ({ tips }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="space-y-3"
  >
    {tips.length === 0 ? (
      <div className="card text-center py-8 text-gray-400">
        No tips available yet.
      </div>
    ) : (
      tips.map((tip, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.1 }}
          className="card"
        >
          <div className="flex items-start gap-3">
            <span className="text-2xl">💡</span>
            <div>
              <h4 className="font-bold text-primary-300">{tip.title}</h4>
              <p className="text-sm text-gray-400 mt-1">{tip.content}</p>
              <div className="flex gap-2 mt-2">
                <span className="text-xs px-2 py-1 bg-dark-700 rounded">{tip.category}</span>
              </div>
            </div>
          </div>
        </motion.div>
      ))
    )}
  </motion.div>
);
