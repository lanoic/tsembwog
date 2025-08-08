import React from 'react';

function Login() {
  return (
    <div className="p-10 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      <form className="space-y-4">
        <input type="email" placeholder="Email" className="w-full p-2 border border-gray-300 rounded" />
        <input type="password" placeholder="Password" className="w-full p-2 border border-gray-300 rounded" />
        <button className="w-full bg-blue-600 text-white py-2 rounded">Login</button>
      </form>
    </div>
  );
}

export default Login;