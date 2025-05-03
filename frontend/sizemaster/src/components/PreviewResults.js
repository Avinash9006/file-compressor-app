import React from "react";

const PreviewResults = ({ file }) => {
  if (!file) return null;

  const { image_base64, format, filename } = file;

  const fileUrl = `data:${format};base64,${image_base64}`;
  const isImage = format.startsWith("image");
  const isPDF = format === "application/pdf";

  return (
    <div className="mt-4">
      <h2 className="text-xl font-semibold mb-2">Preview:</h2>

      {isImage ? (
        <img
          src={fileUrl}
          alt="Preview"
          width={200}
          height={200}
          className="max-w-full h-auto rounded shadow"
        />
      ) : isPDF ? (
        <embed
          src={fileUrl}
          type="application/pdf"
          width="100%"
          height="500px"
          className="rounded border shadow"
        />
      ) : (
        <p className="text-red-500">Unsupported file type.</p>
      )}

      <div className="mt-4">
        <a
          href={fileUrl}
          download={filename.split("/").pop()}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Download File
        </a>
      </div>
    </div>
  );
};

export default PreviewResults;
