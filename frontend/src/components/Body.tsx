import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

interface BlogPost {
  id: number;
  title: string;
  content: string;
  date: string;
  summary?: string;
  tags?: string[];
  media?: string[];
  slug?: string;
}

type BlogPostsResponse = Record<string, BlogPost>;

interface BodyProps {
  refreshTrigger?: number;
}

const Body = ({ refreshTrigger = 0 }: BodyProps): React.ReactElement => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8000/api/blog-posts/');
        if (!response.ok) {
          throw new Error(`Failed to fetch posts: ${response.status}`);
        }
        const data: BlogPostsResponse = await response.json();
        const postsArray = Object.values(data).sort((a, b) => 
          new Date(b.date).getTime() - new Date(a.date).getTime()
        );
        setPosts(postsArray);
        setError(null);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, [refreshTrigger]);

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return isNaN(date.getTime()) ? dateString : date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Loading posts...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow-sm border border-red-200 p-6">
          <div className="flex items-center text-red-700 mb-4">
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            Error loading posts: {error}
          </div>
          <button 
            onClick={() => window.location.reload()} 
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">Recent Posts</h2>
            <p className="text-gray-600 mt-1">Sharing thoughts, ideas, and insights</p>
          </div>
          <span className="text-sm text-gray-500">{posts.length} post{posts.length !== 1 ? 's' : ''}</span>
        </div>

        {posts.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
            <div className="text-gray-400 mb-4">
              <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <p className="text-gray-600 text-xl">No blog posts yet.</p>
            <p className="text-gray-500 mt-2">Click "Write" to create your first post!</p>
          </div>
        ) : (
          posts.map((post) => (
            <article 
              key={post.id} 
              className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
            >
              <div className="p-8">
                <header className="mb-6">
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">{post.title}</h3>
                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    {post.date && (
                      <time dateTime={post.date} className="flex items-center">
                        <svg className="w-2 h-2 mr-1" fill="none" stroke="currentColor" viewBox="0 0 10 10">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        {formatDate(post.date)}
                      </time>
                    )}
                    {post.tags?.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {post.tags.map((tag, index) => (
                          <span 
                            key={index}
                            className="inline-block bg-blue-50 text-blue-700 text-xs px-3 py-1 rounded-full border border-blue-200"
                          >
                            #{tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </header>

                {post.summary && (
                  <div className="mb-6 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                    <p className="text-gray-700 font-medium italic">{post.summary}</p>
                  </div>
                )}

                <div className="prose prose-lg prose-gray max-w-none">
                  <ReactMarkdown>{post.content}</ReactMarkdown>
                </div>
              </div>
            </article>
          ))
        )}
      </div>
    </div>
  );
};

export default Body;