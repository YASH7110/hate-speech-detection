import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { AlertTriangle, MessageSquare, CheckCircle, TrendingUp } from 'lucide-react';

const Dashboard = ({ analyses }) => {
  if (!analyses || analyses.length === 0) {
    return null;
  }

  // Calculate statistics
  const total = analyses.length;
  const hateSpeech = analyses.filter(a => a.prediction.classification === 'hate_speech').length;
  const offensive = analyses.filter(a => a.prediction.classification === 'offensive').length;
  const neutral = analyses.filter(a => a.prediction.classification === 'neutral').length;

  const pieData = [
    { name: 'Hate Speech', value: hateSpeech, color: '#ef4444' },
    { name: 'Offensive', value: offensive, color: '#f97316' },
    { name: 'Neutral', value: neutral, color: '#22c55e' },
  ];

  // Language distribution
  const languageCount = {};
  analyses.forEach(a => {
    const lang = a.prediction.language;
    languageCount[lang] = (languageCount[lang] || 0) + 1;
  });

  const topLanguages = Object.entries(languageCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
        <TrendingUp className="w-6 h-6 mr-2 text-sky-600" />
        Analysis Dashboard
      </h2>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gradient-to-br from-sky-50 to-blue-50 rounded-lg p-4 border border-sky-200">
          <p className="text-sm text-gray-600 mb-1">Total Analyzed</p>
          <p className="text-3xl font-bold text-sky-700">{total}</p>
        </div>
        <div className="bg-gradient-to-br from-red-50 to-pink-50 rounded-lg p-4 border border-red-200">
          <div className="flex items-center justify-between mb-1">
            <p className="text-sm text-gray-600">Hate Speech</p>
            <AlertTriangle className="w-4 h-4 text-red-600" />
          </div>
          <p className="text-3xl font-bold text-red-700">{hateSpeech}</p>
          <p className="text-xs text-gray-500">{((hateSpeech / total) * 100).toFixed(1)}%</p>
        </div>
        <div className="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-lg p-4 border border-orange-200">
          <div className="flex items-center justify-between mb-1">
            <p className="text-sm text-gray-600">Offensive</p>
            <MessageSquare className="w-4 h-4 text-orange-600" />
          </div>
          <p className="text-3xl font-bold text-orange-700">{offensive}</p>
          <p className="text-xs text-gray-500">{((offensive / total) * 100).toFixed(1)}%</p>
        </div>
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg p-4 border border-green-200">
          <div className="flex items-center justify-between mb-1">
            <p className="text-sm text-gray-600">Neutral</p>
            <CheckCircle className="w-4 h-4 text-green-600" />
          </div>
          <p className="text-3xl font-bold text-green-700">{neutral}</p>
          <p className="text-xs text-gray-500">{((neutral / total) * 100).toFixed(1)}%</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Pie Chart */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Classification Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Language Distribution */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Top Languages</h3>
          <div className="space-y-3">
            {topLanguages.map(([lang, count]) => (
              <div key={lang} className="flex items-center space-x-3">
                <span className="text-sm font-medium text-gray-700 w-12">{lang.toUpperCase()}</span>
                <div className="flex-1 h-8 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-sky-500 to-blue-600 flex items-center justify-end pr-2"
                    style={{ width: `${(count / total) * 100}%` }}
                  >
                    <span className="text-xs font-semibold text-white">{count}</span>
                  </div>
                </div>
                <span className="text-sm text-gray-600 w-12 text-right">
                  {((count / total) * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
