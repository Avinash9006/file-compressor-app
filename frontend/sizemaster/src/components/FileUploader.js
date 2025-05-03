import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';

const FileUploader = ({ onDrop, compressFile, isLoading }) => {
  const [file, setFile] = useState(null);
  const [base64Image, setBase64Image] = useState(null);

  const onDropHandler = (acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    setFile(uploadedFile);
    onDrop(acceptedFiles);

    const reader = new FileReader();
    reader.onloadend = () => {
      setBase64Image(reader.result);
    };
    reader.readAsDataURL(uploadedFile);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop: onDropHandler,
    accept: {
      'image/*': [],
      'application/pdf': [],
    },
  });

  const handleRemove = () => {
    setFile(null);
    setBase64Image(null);
  };

  const processFile = () => {
    compressFile()
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-6">
      <div className="w-full max-w-3xl bg-white p-8 rounded-xl shadow-lg space-y-6">
      {isLoading && (
        <div className="flex justify-center mt-4">
          <div className="animate-spin h-10 w-10 border-4 border-t-4 border-blue-500 rounded-full"></div>
        </div>
      )}

        {/* File Drop or Upload Box */}
        {!file ? (
          <div
            {...getRootProps()}
            className="border-4 border-dashed border-blue-500 p-10 text-center bg-gray-50 hover:bg-gray-100 transition-all cursor-pointer"
          >
            <input {...getInputProps()} />
            <p className="text-gray-500 text-xl font-medium">
              📁 Drag & Drop your file here, or click to select
            </p>
          </div>
        ) : (
          <>
            {/* File Info */}
            <div className="text-center">
              <p className="text-lg font-semibold text-green-600">✅ File Uploaded</p>
              <p className="text-gray-700 mt-1">
                <span className="font-medium">Name:</span> {file.name}
              </p>
              <p className="text-gray-500">
                <span className="font-medium">Size:</span> {(file.size / 1024).toFixed(2)} KB
              </p>
            </div>

            {/* File Preview */}
            {base64Image && file.type.startsWith("image/") && (
              <img
                src={base64Image}
                alt="Preview"
                className="rounded-lg shadow-lg mx-auto max-h-[400px]"
              />
            )}

            {base64Image && file.type === "application/pdf" && (
              <div className="rounded-lg overflow-hidden shadow">
                <embed
                  src={base64Image}
                  type="application/pdf"
                  width="100%"
                  height="400px"
                />
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex justify-center gap-4">
              <button
                onClick={handleRemove}
                className="px-5 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
              >
                Remove
              </button>
              <button
                onClick={processFile}
                className="px-5 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Process File
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default FileUploader;
