import React, { useState } from 'react';
import axios from 'axios';
import './ImageUpload.css'; // Import the CSS file for styling

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState('');
  const [labels, setLabels] = useState(['']);
  const [predictions, setPredictions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setImage(file);
      setImagePreviewUrl(URL.createObjectURL(file));
    }
  };
  const handleLabelChange = (index, e) => {
    const newLabels = labels.map((label, i) => {
      if (index === i) {
        return e.target.value;
      }
      return label;
    });
    setLabels(newLabels);
  };

  const handleAddLabel = () => {
    setLabels([...labels, '']);
  };

  const handleRemoveLabel = (index) => {
    const newLabels = labels.filter((_, i) => i !== index);
    setLabels(newLabels);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const formData = new FormData();
    formData.append('image', image);
    formData.append('labels', labels.join(',')); 

    try {
      const response = await axios.post('http://localhost:8000/inference', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setPredictions(response.data.data);
    } catch (error) {
      console.error('Error uploading:', error);
      setPredictions([]);
    }
    setIsLoading(false);
  };

  return (
    <div className="upload-container">
      <form onSubmit={handleSubmit} className="upload-form">
        <input type="file" onChange={handleImageChange} className="file-input" />
        {imagePreviewUrl && <img src={imagePreviewUrl} alt="Preview" className="image-preview"/>}
        <div className="label-section">
          {labels.map((label, index) => (
            <div key={index} className="label-input-group">
              <input
                type="text"
                value={label}
                onChange={(e) => handleLabelChange(index, e)}
                className="text-input"
                placeholder="Enter a label"
              />
              {labels.length > 1 && (
                <button type="button" onClick={() => handleRemoveLabel(index)} className="remove-btn">
                  &times;
                </button>
              )}
            </div>
          ))}
          <button type="button" onClick={handleAddLabel} className="add-btn">
            Add Label
          </button>
        </div>
        <button type="submit" disabled={isLoading} className="submit-btn">
          {isLoading ? 'Predicting...' : 'Predict Image'}
        </button>
      </form>

      {predictions.length > 0 && (
  <div className="prediction-results">
    <h3>Prediction Results:</h3>
    <ul>
      {predictions.map((prediction, index) => (
        <li key={index} className="prediction-item">
          <strong>{prediction.class}</strong>: {Math.round(parseFloat(prediction.probability) * 100)}%
        </li>
      ))}
    </ul>
  </div>
)}


 </div>
 );
};

export default ImageUpload;