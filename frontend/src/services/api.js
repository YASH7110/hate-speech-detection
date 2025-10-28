import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Prediction API
export const predictSingle = async (text) => {
  const response = await api.post('/predict/single', { text });
  return response.data;
};

export const predictBatch = async (comments) => {
  const response = await api.post('/predict/batch', { comments });
  return response.data;
};

// Twitter API
export const searchTweets = async (keyword, maxResults = 100) => {
  const response = await api.get('/twitter/search', {
    params: { keyword, max_results: maxResults }
  });
  return response.data;
};

export const getUserTweets = async (username, maxResults = 100) => {
  const response = await api.get(`/twitter/user/${username}`, {
    params: { max_results: maxResults }
  });
  return response.data;
};

// YouTube API
export const getVideoComments = async (videoUrl, maxResults = 100) => {
  const response = await api.get('/youtube/video', {
    params: { video_url: videoUrl, max_results: maxResults }
  });
  return response.data;
};

export const getChannelComments = async (channelId, maxResults = 100) => {
  const response = await api.get(`/youtube/channel/${channelId}`, {
    params: { max_results: maxResults }
  });
  return response.data;
};

export default api;

