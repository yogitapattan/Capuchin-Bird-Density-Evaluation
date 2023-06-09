import axios from 'axios';

export const evaluateCapuchinDensity = (audioFile) => {
    const url = 'http://127.0.0.1:8000/capuchin'

    const formData = new FormData();
    formData.append('file', audioFile);
    
    return axios.post(url, formData);
}