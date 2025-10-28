import React, { useState } from 'react';
import { Search, Twitter, Youtube } from 'lucide-react';

const SearchBar = ({ onSearch, loading }) => {
  const [platform, setPlatform] = useState('twitter');
  const [searchQuery, setSearchQuery] = useState('');
  const [maxResults, setMaxResults] = useState(100);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onSearch(platform, searchQuery, maxResults);
    }
  };

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-6 mb-8">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Platform Selection */}
        <div className="flex space-x-4">
          <button
            type="button"
            onClick={() => setPlatform('twitter')}
            className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 rounded-lg font-semibold transition-all ${
              platform === 'twitter'
                ? 'bg-sky-600 text-white shadow-lg'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <Twitter className="w-5 h-5" />
            <span>Twitter</span>
          </button>
          <button
            type="button"
            onClick={() => setPlatform('youtube')}
            className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 rounded-lg font-semibold transition-all ${
              platform === 'youtube'
                ? 'bg-red-600 text-white shadow-lg'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <Youtube className="w-5 h-5" />
            <span>YouTube</span>
          </button>
        </div>

        {/* Search Input */}
        <div className="relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={
              platform === 'twitter'
                ? 'Enter keyword or @username'
                : 'Enter YouTube video URL or channel ID'
            }
            className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-sky-500 focus:outline-none transition-colors"
          />
        </div>

        {/* Max Results */}
        <div className="flex items-center space-x-4">
          <label className="text-sm font-medium text-gray-700">
            Max Results: {maxResults}
          </label>
          <input
            type="range"
            min="10"
            max="100"
            step="10"
            value={maxResults}
            onChange={(e) => setMaxResults(Number(e.target.value))}
            className="flex-1"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !searchQuery.trim()}
          className="w-full bg-gradient-to-r from-sky-500 to-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-sky-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
        >
          {loading ? 'Analyzing...' : 'Analyze Comments'}
        </button>
      </form>
    </div>
  );
};

export default SearchBar;
