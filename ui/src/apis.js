
import axios from 'axios';
const getHostPort = () => {
    if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
        // dev code
        var host = '127.0.0.1';
        var port = '8000';

    } else {
        // production code
        var host = window.location.hostname;
        var port = window.location.port;
    }
    return [host, port];
}
const [host, port] = getHostPort();

const staticRoot = `http://${host}:${port}/static`;
const baseURL = `http://${host}:${port}`;
const streamURL = `http://${host}:${port}/stream`;
const axiosRoot = axios.create({
    baseURL: baseURL,
    timeout: 3000000,
});
const getStatusAPI = async () => {
    const response = await axiosRoot.get('/status');
    console.log(response.data)
    return response.data;
}
const setVLMPromptAPI = async (prompt) => {
    const response = await axiosRoot.post('/vlm_prompt', { prompt: prompt });
    return response.data;
}
const setVMPromptAPI = async (prompt) => {
    const response = await axiosRoot.post('/vm_prompt', { prompt: prompt });
    return response.data;
}


export {
    staticRoot,
    streamURL,
    setVLMPromptAPI,
    setVMPromptAPI,
    getStatusAPI

};