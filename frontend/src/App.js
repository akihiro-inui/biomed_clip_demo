import React from 'react';
import ImageUpload from './components/ImageUpload'; // Import the ImageUpload component
import './App.css'; // Importing CSS for styling

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Medical Image Predictor</h1>
        <ImageUpload />
      </header>
    </div>
  );
}

export default App;
