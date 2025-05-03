import React, { useState, useEffect } from "react";

const AutoFixSpecs = ({ file, formSpecs }) => {
  const [modifiedFile, setModifiedFile] = useState(null);
  const [error, setError] = useState(null);

  // Function to apply compression and resize
  const applyFixes = (file, specs) => {
    // Create FormData to send file and form specs to backend
    const formData = new FormData();
    formData.append("file", file);
    formData.append("specs", JSON.stringify(specs));

    // Call backend API for auto-fixing
    fetch("/api/fix-specs", {
      method: "POST",
      body: formData,
    })
      .then(response => response.blob())
      .then(blob => {
        const fixedFile = new File([blob], file.name, { type: file.type });
        setModifiedFile(fixedFile);
      })
      .catch(error => {
        console.error("Error fixing file specs:", error);
        setError("There was an error applying the specifications.");
      });
  };

  useEffect(() => {
    if (file && formSpecs) {
      applyFixes(file, formSpecs); // Apply fix when file or specs are updated
    }
  }, [file, formSpecs]);

  // File type detection for preview
  const isImage = file?.type.startsWith("image");
  const isPDF = file?.type === "application/pdf";

  // Preview the modified file
  const fileUrl = modifiedFile ? URL.createObjectURL(modifiedFile) : null;

  return (
    <div className="auto-fix-specs">
      {error && <p className="text-red-500">{error}</p>}

      {fileUrl && (
        <div className="preview">
          <h3>Preview of Fixed File</h3>
          {isImage ? (
            <img src={fileUrl} alt="Fixed File" className="max-w-full h-auto" />
          ) : isPDF ? (
            <embed
              src={fileUrl}
              width="600"
              height="400"
              type="application/pdf"
              title="Fixed PDF"
            />
          ) : (
            <p>Unsupported file type for preview.</p>
          )}
        </div>
      )}

      {modifiedFile && (
        <div className="download-btn mt-4">
          <a
            href={fileUrl}
            download={modifiedFile.name}
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            Download Fixed File
          </a>
        </div>
      )}
    </div>
  );
};

export default AutoFixSpecs;
