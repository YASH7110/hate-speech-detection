// import React from 'react';
// import { AlertTriangle, MessageSquare, CheckCircle, Globe } from 'lucide-react';

// const CommentCard = ({ analysis }) => {
//   const { comment, prediction } = analysis;

//   const getClassificationColor = (classification) => {
//     switch (classification) {
//       case 'hate_speech':
//         return 'bg-red-100 border-red-300 text-red-800';
//       case 'offensive':
//         return 'bg-orange-100 border-orange-300 text-orange-800';
//       case 'neutral':
//         return 'bg-green-100 border-green-300 text-green-800';
//       default:
//         return 'bg-gray-100 border-gray-300 text-gray-800';
//     }
//   };

//   const getClassificationIcon = (classification) => {
//     switch (classification) {
//       case 'hate_speech':
//         return <AlertTriangle className="w-5 h-5" />;
//       case 'offensive':
//         return <MessageSquare className="w-5 h-5" />;
//       case 'neutral':
//         return <CheckCircle className="w-5 h-5" />;
//       default:
//         return null;
//     }
//   };

//   return (
//     <div className="bg-white/90 backdrop-blur-sm rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
//       {/* Header */}
//       <div className="flex items-start justify-between mb-3">
//         <div className="flex items-center space-x-2">
//           <div className={`p-2 rounded-full ${getClassificationColor(prediction.classification)}`}>
//             {getClassificationIcon(prediction.classification)}
//           </div>
//           <div>
//             <p className="font-semibold text-gray-900">{comment.author}</p>
//             <p className="text-xs text-gray-500">
//               {new Date(comment.timestamp).toLocaleString()}
//             </p>
//           </div>
//         </div>
//         <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getClassificationColor(prediction.classification)}`}>
//           {prediction.classification.replace('_', ' ').toUpperCase()}
//         </span>
//       </div>

//       {/* Comment Text */}
//       <p className="text-gray-700 mb-3 leading-relaxed">{comment.text}</p>

//       {/* Metrics */}
//       <div className="flex items-center justify-between pt-3 border-t border-gray-200">
//         <div className="flex items-center space-x-4">
//           <div className="flex items-center space-x-1">
//             <Globe className="w-4 h-4 text-sky-600" />
//             <span className="text-sm text-gray-600">
//               {prediction.language.toUpperCase()}
//             </span>
//           </div>
//           <span className="text-xs text-gray-400">
//             {(prediction.language_confidence * 100).toFixed(1)}% lang confidence
//           </span>
//         </div>
//         <div className="flex items-center space-x-2">
//           <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
//             <div
//               className={`h-full ${
//                 prediction.classification === 'hate_speech'
//                   ? 'bg-red-500'
//                   : prediction.classification === 'offensive'
//                   ? 'bg-orange-500'
//                   : 'bg-green-500'
//               }`}
//               style={{ width: `${prediction.confidence * 100}%` }}
//             />
//           </div>
//           <span className="text-xs font-semibold text-gray-700">
//             {(prediction.confidence * 100).toFixed(1)}%
//           </span>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default CommentCard;


import React, { useState } from 'react';
import { AlertTriangle, MessageSquare, CheckCircle, Globe, ThumbsUp, ThumbsDown } from 'lucide-react';
import axios from 'axios';

const CommentCard = ({ analysis }) => {
  const { comment, prediction } = analysis;
  const [feedbackGiven, setFeedbackGiven] = useState(false);
  const [feedbackType, setFeedbackType] = useState(null);

  const getClassificationColor = (classification) => {
    switch (classification) {
      case 'hate_speech':
        return 'bg-red-100 border-red-300 text-red-800';
      case 'offensive':
        return 'bg-orange-100 border-orange-300 text-orange-800';
      case 'neutral':
        return 'bg-green-100 border-green-300 text-green-800';
      default:
        return 'bg-gray-100 border-gray-300 text-gray-800';
    }
  };

  const getClassificationIcon = (classification) => {
    switch (classification) {
      case 'hate_speech':
        return <AlertTriangle className="w-5 h-5" />;
      case 'offensive':
        return <MessageSquare className="w-5 h-5" />;
      case 'neutral':
        return <CheckCircle className="w-5 h-5" />;
      default:
        return null;
    }
  };

  const handleFeedback = async (isCorrect) => {
    try {
      const response = await axios.post('http://localhost:8000/api/predict/feedback', {
        comment_id: comment.id || `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        text: comment.text,
        predicted_classification: prediction.classification,
        is_correct: isCorrect,
        confidence: prediction.confidence,
        language: prediction.language
      });

      setFeedbackGiven(true);
      setFeedbackType(isCorrect ? 'correct' : 'incorrect');
      
      console.log(response.data.message);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    }
  };

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          <div className={`p-2 rounded-full ${getClassificationColor(prediction.classification)}`}>
            {getClassificationIcon(prediction.classification)}
          </div>
          <div>
            <p className="font-semibold text-gray-900">{comment.author}</p>
            <p className="text-xs text-gray-500">
              {new Date(comment.timestamp).toLocaleString()}
            </p>
          </div>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getClassificationColor(prediction.classification)}`}>
          {prediction.classification.replace('_', ' ').toUpperCase()}
        </span>
      </div>

      {/* Comment Text */}
      <p className="text-gray-700 mb-3 leading-relaxed">{comment.text}</p>

      {/* Metrics */}
      <div className="flex items-center justify-between pt-3 border-t border-gray-200">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1">
            <Globe className="w-4 h-4 text-sky-600" />
            <span className="text-sm text-gray-600">
              {prediction.language.toUpperCase()}
            </span>
          </div>
          <span className="text-xs text-gray-400">
            {(prediction.language_confidence * 100).toFixed(1)}% lang confidence
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className={`h-full ${
                prediction.classification === 'hate_speech'
                  ? 'bg-red-500'
                  : prediction.classification === 'offensive'
                  ? 'bg-orange-500'
                  : 'bg-green-500'
              }`}
              style={{ width: `${prediction.confidence * 100}%` }}
            />
          </div>
          <span className="text-xs font-semibold text-gray-700">
            {(prediction.confidence * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      {/* Feedback Section */}
      <div className="flex items-center justify-end pt-3 border-t border-gray-200 mt-3">
        {!feedbackGiven ? (
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-500">Was this prediction correct?</span>
            <button
              onClick={() => handleFeedback(true)}
              className="flex items-center gap-1 px-3 py-1.5 bg-green-50 hover:bg-green-100 text-green-700 rounded-lg transition-colors text-sm font-medium"
              title="Mark as correct"
            >
              <ThumbsUp className="w-4 h-4" />
              Yes
            </button>
            <button
              onClick={() => handleFeedback(false)}
              className="flex items-center gap-1 px-3 py-1.5 bg-red-50 hover:bg-red-100 text-red-700 rounded-lg transition-colors text-sm font-medium"
              title="Mark as incorrect"
            >
              <ThumbsDown className="w-4 h-4" />
              No
            </button>
          </div>
        ) : (
          <div className={`text-sm font-medium ${feedbackType === 'correct' ? 'text-green-600' : 'text-orange-600'}`}>
            ✓ Feedback recorded. Thank you!
          </div>
        )}
      </div>
    </div>
  );
};

export default CommentCard;
