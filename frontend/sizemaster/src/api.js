// src/api.js
import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

// Fetch form specifications
export const fetchFormSpecs = async () => {
    return axios.get(`${API_BASE_URL}/form-specs`);
};

// Compress uploaded file based on form specs
export const compressFile = async (file, formSpecs) => {
    // background color :  #cdcdcd
    const formData = new FormData();
    formData.append("file", file);
    formData.append("width", 600);
    formData.append("height", 600);
    formData.append("quality", 90);
    formData.append("format", 'jpeg');
    formData.append("remove_bg", true);
    //   formData.append("formSpecs", JSON.stringify(formSpecs));

    return axios.post(`${API_BASE_URL}/resize`, formData, {
        headers: {
            "Content-Type": "multipart/form-data"
        }
    });
};
