import React, { useState } from 'react';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import Dashboard from './components/Dashboard';
import CommentCard from './components/CommentCard';
import ButterflyGarden from './components/Butterfly';
import { searchTweets, getUserTweets, getVideoComments, getChannelComments } from './services/api';
import { AlertCircle } from 'lucide-react';

function App() {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (platform, query, maxResults) => {
    setLoading(true);
    setError(null);
    setAnalyses([]);

    try {
      let results;
      
      if (platform === 'twitter') {
        if (query.startsWith('@')) {
          const username = query.slice(1);
          results = await getUserTweets(username, maxResults);
        } else {
          results = await searchTweets(query, maxResults);
        }
      } else if (platform === 'youtube') {
        if (query.includes('youtube.com') || query.includes('youtu.be')) {
          results = await getVideoComments(query, maxResults);
        } else {
          results = await getChannelComments(query, maxResults);
        }
      }

      setAnalyses(results);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError(err.response?.data?.detail || 'Failed to fetch and analyze comments. Please check your API credentials and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen sky-gradient relative overflow-hidden">
      <ButterflyGarden count={8} />

      <div className="cloud fixed top-20 left-10 w-32 h-12 opacity-70" style={{ animationDelay: '0s' }}></div>
      <div className="cloud fixed top-40 right-20 w-24 h-10 opacity-60" style={{ animationDelay: '3s' }}></div>
      <div className="cloud fixed top-60 left-1/4 w-28 h-11 opacity-50" style={{ animationDelay: '6s' }}></div>

      <div className="relative z-20">
        <Header />

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <SearchBar onSearch={handleSearch} loading={loading} />

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-8 flex items-center">
              <AlertCircle className="w-5 h-5 mr-2" />
              <span>{error}</span>
            </div>
          )}

          {loading && (
            <div className="flex flex-col items-center justify-center py-12">
              <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-sky-600 mb-4"></div>
              <p className="text-lg text-gray-700 font-medium">Analyzing comments...</p>
            </div>
          )}

          {!loading && analyses.length > 0 && (
            <>
              <Dashboard analyses={analyses} />

              <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                  Analyzed Comments ({analyses.length})
                </h2>
                <div className="space-y-4 max-h-[800px] overflow-y-auto">
                  {analyses.map((analysis, index) => (
                    <CommentCard key={index} analysis={analysis} />
                  ))}
                </div>
              </div>
            </>
          )}

          {!loading && !error && analyses.length === 0 && (
            <div className="text-center py-12">
              <p className="text-lg text-gray-600">
                Enter a keyword, username, or video URL to start analyzing comments for hate speech.
              </p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
