import React from "react";
import UserInfoCard from "./components/UserInfoCard";
import AIResponseCard from "./components/AIResponseCard";

function App() {
  return (
    <div className="w-full min-h-screen bg-gray-50 p-4">
      <div className="max-w-md mx-auto space-y-4">
        <UserInfoCard />
        <AIResponseCard />
      </div>
    </div>
  );
}

export default App;