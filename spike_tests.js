import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check } from 'k6';

const statusTrend = new Trend('status_codes');

export const options = {
    // Tu configuración de Traefik redirige a HTTPS y usa un certificado auto-firmado.
    insecureSkipTLSVerify: true,
    // AJUSTE CRÍTICO: Reducimos la carga a un nivel manejable (20 usuarios).
    // 10,000 usuarios saturarán el servidor de desarrollo y causarán timeouts.
    stages: [
        { duration: "10s", target: 1000 },
        { duration: "20s", target: 1000 },
        { duration: "5s", target: 0 },
    ],
};

export default function () {
    // Apuntamos al entrypoint HTTPS de Traefik.
    const BASE_URL = 'https://alumnos.universidad.localhost';
    };

    // 2. Cambia la petición a un GET hacia un endpoint válido, como '/alumno'.
    //    No necesitamos 'payload' ni 'params' para una petición GET simple.
    const res = http.get(`${BASE_URL}/alumno/1/`); // Ejemplo: obtener el alumno con ID 1
   

    
    statusTrend.add(res.status);

    check(res, {
        'status is 200': (r) => r.status === 200, // El endpoint /alumno debería devolver 200 OK
        'status is not 500': (r) => r.status !== 500, // Verificamos que no haya errores internos del servidor
    });
}
