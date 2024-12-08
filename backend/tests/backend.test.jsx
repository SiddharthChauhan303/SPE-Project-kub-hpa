const request = require('supertest');
const http = require('http');
const app = require('../index');

let server;

beforeAll((done) => {
    server = http.createServer(app);
    server.listen(3000, () => {
        console.log('Test server started on port 3000');
        done();
    });
});

afterAll((done) => {
    server.close(() => {
        console.log('Test server closed');
        done();
    });
});

describe('Backend API Tests', () => {
    it('should return 400 if fileName is not provided', async () => {
        const res = await request(server).post('/read-csv').send({});
        expect(res.statusCode).toBe(400);
        expect(res.body).toHaveProperty('error', 'fileName is required');
    });

    it('should return 404 if file is not found', async () => {
        const res = await request(server).post('/read-csv').send({ fileName: 'nonexistent.csv' });
        expect(res.statusCode).toBe(404);
        expect(res.body).toHaveProperty('error');
    });

    it('should execute Python script and return valid JSON', async () => {
        const res = await request(server).post('/sample');
        expect(res.statusCode).toBe(200);
        expect(Array.isArray(res.body)).toBe(true);
    });
});
