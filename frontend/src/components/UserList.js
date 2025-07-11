import React from 'react';

function UserList({ users }) {
  if (!users || users.length === 0) {
    return (
      <div className="loading">
        No users found. Create your first user to get started!
      </div>
    );
  }

  return (
    <div>
      {users.map(user => (
        <div key={user.id} className="list-item">
          <h4>{user.name}</h4>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>ID:</strong> {user.id}</p>
          <p><strong>Created:</strong> {
            user.created_at 
              ? new Date(user.created_at).toLocaleDateString() 
              : 'Unknown'
          }</p>
        </div>
      ))}
    </div>
  );
}

export default UserList;