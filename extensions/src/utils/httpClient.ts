export class HttpClient {
    public async sendRequest(url: string, method: string, headers: Record<string, string>, body?: string | FormData) {
        console.log("Request sent from https client");
        try {
            const options: RequestInit = {
                method,
                headers,
            };

            if (body) {
                if (body instanceof FormData) {
                    options.body = body;
                    // Remove content-type header as it will be set automatically for FormData
                    delete options.headers['content-type'];
                } else if (typeof body === 'string') {
                    options.body = body;
                }
            }

            const response = await fetch(url, options);

            const responseHeaders: Record<string, string> = {};
            response.headers.forEach((value, key) => {
                responseHeaders[key] = value;
            });

            const responseBody = await response.text(); // Get the response body as text

            return {
                status: response.status,
                statusText: response.statusText,
                headers: responseHeaders,
                body: responseBody,
            };
        } catch (error) {
            console.error('Error sending request:', error);
            throw error; // Re-throw the error for further handling
        }
    }
}