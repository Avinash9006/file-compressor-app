import React, { useState } from "react";
import { compressFile } from "./api";
import FormSelector from "./components/FormSelector";
import FileUploader from "./components/FileUploader";
import PreviewResults from "./components/PreviewResults";
import "./App.css";

const App = () => {
  const [formSpecs, setFormSpecs] = useState(null);         // Selected form spec
  const [file, setFile] = useState(null);                   // Uploaded file
  const [compressedFile, setCompressedFile] = useState(null); // Base64 result
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const handleFileDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setCompressedFile(null); // Reset old preview
  };

  const handleCompressFile = async () => {
    if (!file || !formSpecs) {
      alert("Please select a form and upload a file.");
      return;
    }

    setIsLoading(true);

    try {
      const response = await compressFile(file, formSpecs);
      setCompressedFile(response.data); // Expecting base64 image string from backend
      setIsLoading(false);
    } catch (error) {
      console.error("Compression failed:", error);
      alert("File compression failed. Try again.");
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-3xl">
      <h1 className="text-2xl font-bold mb-6 text-center">Photo Compression & Passport Generator</h1>

      <FormSelector setFormSpecs={setFormSpecs} />

      <FileUploader onDrop={handleFileDrop} compressFile={handleCompressFile} isLoading={isLoading} />

      {compressedFile && (
        <div className="mt-8">
          <h2 className="text-xl font-semibold mb-4">Result Preview:</h2>
          <PreviewResults file={compressedFile} />
        </div>
      )}
    </div>
  );
};

export default App;
