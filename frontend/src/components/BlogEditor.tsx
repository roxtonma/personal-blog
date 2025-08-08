import { useState } from 'react';
import MDEditor from '@uiw/react-md-editor';
import '@uiw/react-md-editor/markdown-editor.css';

interface BlogEditorProps {
  onPostCreated: () => void;
  onNavigate: (page: string) => void;
}

const BlogEditor = ({ onPostCreated, onNavigate }: BlogEditorProps) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    setSuccess('');
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/blog-posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content }),
      });

      if (response.ok) {
        setSuccess('Blog post published successfully!');
        setTitle('');
        setContent('');
        onPostCreated();
        setTimeout(() => {
          onNavigate('home');
        }, 2000);
      } else {
        const data = await response.json().catch(() => ({}));
        setError(data.detail || 'Error creating blog post');
      }
    } catch (err) {
      setError((err as Error).message || 'Network error');
    } finally {
      setLoading(false);
      setTimeout(() => {
        setSuccess('');
        setError('');
      }, 4000);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-white">
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4 bg-gray-50 flex-shrink-0 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => onNavigate('home')}
            className="flex items-center text-gray-600 hover:text-gray-900 transition"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div className="h-6 w-px bg-gray-300"></div>
          <h2 className="text-lg font-semibold text-gray-900">Write New Post</h2>
        </div>

        <div className="flex items-center space-x-3">
          {success && (
            <div className="flex items-center text-green-700 text-sm">
              ✅ {success}
            </div>
          )}
          {error && (
            <div className="flex items-center text-red-700 text-sm">
              ❌ {error}
            </div>
          )}
          <button
            onClick={handleSubmit}
            className="px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={loading || !title.trim() || !content.trim()}
          >
            {loading ? 'Publishing...' : 'Publish'}
          </button>
        </div>
      </div>

      {/* Title Input */}
      <div className="px-6 py-4 border-b border-gray-200 flex-shrink-0">
        <input
          className="w-full text-3xl font-bold placeholder-gray-400 border-0 focus:outline-none focus:ring-0 bg-transparent"
          placeholder="Post title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={loading}
        />
      </div>

      {/* Markdown Editor */}
      <div className="flex-1 min-h-0 p-6 bg-white">
        <div className="h-full">
          <MDEditor
            value={content}
            onChange={(val) => setContent(val || '')}
            preview="edit"
            hideToolbar={false}
            visibleDragbar={false}
            textareaProps={{
              placeholder: 'Start writing your post in markdown...',
              style: {
                fontSize: 14,
                lineHeight: 1.6,
                fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
              },
              disabled: loading,
            }}
            height={400}
            data-color-mode="light"
          />
        </div>
      </div>
    </div>
  );
};

export default BlogEditor;