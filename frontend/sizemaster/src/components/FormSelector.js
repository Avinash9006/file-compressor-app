// src/components/FormSelector.jsx
import React, { useEffect, useState } from "react";
import { fetchFormSpecs } from "../api";

const FormSelector = ({ setFormSpecs }) => {
  const [options, setOptions] = useState([]);

  useEffect(() => {
    fetchFormSpecs()
      .then((response) => {
        setOptions(response.data.data); // assuming response is an array of specs
      })
      .catch((error) => console.error("Failed to load form specs:", error));
  }, []);

  const handleChange = (e) => {
    const selected = options.find(opt => opt.name === e.target.value);
    setFormSpecs(selected || null);
  };

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-2">Select Form Type:</label>
      <select
        onChange={handleChange}
        className="border border-gray-300 rounded px-4 py-2"
        defaultValue=""
      >
        <option value="" disabled>Select a form</option>
        {options.map((opt, idx) => (
          <option key={idx} value={opt.name}>
            {opt.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default FormSelector;
