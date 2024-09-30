import { useQuery } from 'react-query';
import axios from 'axios';

const UseSendToLLM = (endpoint, formData) => {
  return useQuery(
    ['UseSendToLLM', endpoint, formData],
    async () => {
      const { data } = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return data;
    },
    {
      staleTime: 5 * 60 * 1000, 
      cacheTime: 10 * 60 * 1000, 
      refetchOnWindowFocus: false, 
    }
  );
};

export default UseSendToLLM;
