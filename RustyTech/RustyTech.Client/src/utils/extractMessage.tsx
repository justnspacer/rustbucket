/* eslint-disable @typescript-eslint/no-explicit-any */

const extractMessage = (response: any): string => {
    if (response?.data?.data?.message) {
        return response.data.data.message;
    } else if (response?.title) {
        return response.title;
    } else {
        return 'An unexpected error occurred. Please try again.';
    }
};

export default extractMessage;