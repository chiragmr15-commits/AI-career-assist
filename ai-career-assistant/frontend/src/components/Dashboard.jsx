import React from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export const Dashboard = () => {
  const [stats, setStats] = React.useState({
    atsScore: 75,
    interviewScore: 68,
    careerReadiness: 82,
    emotionalHealth: 70,
  });

  const [moodData, setMoodData] = React.useState([
    { day: 'Mon', mood: 7, stress: 4 },
    { day: 'Tue', mood: 6, stress: 5 },
    { day: 'Wed', mood: 8, stress: 3 },
    { day: 'Thu', mood: 7, stress: 4 },
    { day: 'Fri', mood: 9, stress: 2 },
    { day: 'Sat', mood: 8, stress: 1 },
    { day: 'Sun', mood: 8, stress: 2 },
  ]);

  const statCards = [
    { label: 'ATS Score', value: stats.atsScore, icon: '📄' },
    { label: 'Interview Score', value: stats.interviewScore, icon: '🎤' },
    { label: 'Career Readiness', value: stats.careerReadiness, icon: '🚀' },
    { label: 'Emotional Health', value: stats.emotionalHealth, icon: '❤️' },
  ];

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-bold gradient-text">Your Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="card"
          >
            <div className="text-4xl mb-2">{stat.icon}</div>
            <div className="text-gray-400 text-sm">{stat.label}</div>
            <div className="text-3xl font-bold text-primary-400">{stat.value}%</div>
            <div className="h-1 bg-dark-700 rounded-full mt-3 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${stat.value}%` }}
                transition={{ delay: 0.5, duration: 1 }}
                className="h-full bg-gradient-to-r from-primary-500 to-blue-600"
              />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card"
        >
          <h3 className="text-xl font-bold mb-4">Weekly Mood & Stress</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={moodData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
              <Legend />
              <Line type="monotone" dataKey="mood" stroke="#3b82f6" strokeWidth={2} />
              <Line type="monotone" dataKey="stress" stroke="#ef4444" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card"
        >
          <h3 className="text-xl font-bold mb-4">Skill Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={[
                  { name: 'Technical', value: 40 },
                  { name: 'Soft Skills', value: 30 },
                  { name: 'Others', value: 30 },
                ]}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                dataKey="value"
              >
                <Cell fill="#3b82f6" />
                <Cell fill="#10b981" />
                <Cell fill="#f59e0b" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <ActionButton icon="📤" label="Upload Resume" href="/resume" />
          <ActionButton icon="💼" label="Get Recommendation" href="/career" />
          <ActionButton icon="🎤" label="Practice Interview" href="/interview" />
          <ActionButton icon="📔" label="Log Mood" href="/emotion" />
        </div>
      </motion.div>
    </div>
  );
};

const ActionButton = ({ icon, label, href }) => (
  <a href={href} className="flex flex-col items-center justify-center p-4 rounded-lg hover:bg-white/10 transition-colors">
    <div className="text-3xl mb-2">{icon}</div>
    <div className="text-xs text-center text-gray-300">{label}</div>
  </a>
);
