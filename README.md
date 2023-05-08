# Universidad de Guadalajara - Centro Universitario de Ciencias Exactas e Ingenierías


## Departamento de ciencias computacionales
Computación tolerante a fallas - Sección D06
Profesor: *López Franco Michel Emanuel*
Alumno: *Lomelí Flores Jesús Isaac*

## Kubernetes


### Introducción


### ¿Qué es Kubernetes?  

<p align="justify">
Kubernetes es una plataforma portable y extensible de código abierto para administrar cargas de trabajo y servicios. Kubernetes facilita la automatización y la configuración declarativa. 
</p>
<p align="justify"> 
Kubernetes ofrece un entorno de administración centrado en contenedores. Orquesta la infraestructura de cómputo, redes y almacenamiento para que las cargas de trabajo de los usuarios no tengan que hacerlo. Esto ofrece la simplicidad de las Plataformas como Servicio (PaaS) con la flexibilidad de la Infraestructura como Servicio (IaaS) y permite la portabilidad entre proveedores de infraestructura.
</p>


### ¿Qué es Ingress?  

<p align="justify">
Es un objeto de Kubernetes que gestiona el acceso externo a los servicios del clúster de Kubernetes. Expone rutas HTTP y HTTPS desde fuera del clúster de Kubernetes a los servicios del clúster de Kubernetes.
</p>

<p align="justify">
Para utilizar Ingress, debes tener el Controlador Ingress en el clúster Kubernetes. No viene como parte del clúster de Kubernetes como otros controladores del clúster, no se inicia automáticamente en el clúster. Podemos desplegar cualquier número de controladores de ingreso en el clúster de Kubernetes.
</p>


### ¿Qué es un LoadBalancer?

<p align="justify">
Distribuye automáticamente el tráfico entrante entre varios destinos, por ejemplo, instancias EC2, contenedores y direcciones IP en una o varias zonas de disponibilidad. Monitorea el estado de los destinos registrados y enruta el tráfico solamente a destinos en buen estado. Load Balancing escala el balanceador de carga a medida que el tráfico entrante va cambiando con el tiempo. Puede escalarse automáticamente para adaptarse a la mayoría de las cargas de trabajo.
</p>

### Desarrollo

<p align="justify">
Para comenzar a utilizar kubernetes lo primero que se realizo fue instalar minikube y posterioemente se inicializo tal como se observa en la siguiente captura.
</p>

![Minikube start](/Imagenes/Screenshot_47.png)

<p align="justify">
Para esta practica se utilizo una API sencilla realizada en python con FastAPI cuyo codigo principal es el siguiente. 
</p>

```py
from fastapi import FastAPI
from router import libros

app = FastAPI(
    title='API-Kubernetes',
    description='API para materia tolerante a fallas',
    version='1.0.0'
)

app.include_router(libros.router)

@app.on_event("startup")
def startup():
    print("Iniciando servidor")


@app.on_event("shutdown")
def shutdown():
    print("Cerrando servidor")


@app.get('/')
async def root():
    return { 'root' : 'hola' }
```

<p align="justify">
La API cuenta con una ruta desde la cual se permite obtener libros almacenados en un archivo. Las maneras de obtencion son de todos los libros a la vez o 1 en especifico por medio del ID.
</p>


<p align="justify">
Una vez explicada la API que sera utilizada, retomo la descripcion del proceso mencionando la creacion de dos archivos .yaml, uno para crear el servicio y otro para el despliegue.
</p>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-kubernetes-jilf
  labels:
    app: apikubernetes
spec:
  replicas: 4
  selector:
    matchLabels:
      app: apikubernetes
  template:
    metadata:
      labels:
        app: apikubernetes
    spec:
      containers:
      - name: apikubernetes
        image: caasi81/apikubernetes:v1
        ports:
        - containerPort: 8080
```


```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-kubernetes-jilf
  labels:
    app: api-kubernetes-jilf
spec:
  type: LoadBalancer
  selector:
    app: apikubernetes
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  sessionAffinity: None
```

<p align="justify">
Una vez creados estos archivos se crea la imagen autilizar, asi como el servicio y despliegue con ayuda de los archivos creados. Finalmente se expone el puerto y se obtiene el puerto en el cual se esta ejecutando la API
</p>


![Creación de servicio](/Imagenes/Screenshot_50.png)


<p align="justify">
Para confirmar que la API sea accesible se ingresa desde el localhost en el puerto obtenido con anterioridad y se ingresa a una ruta valida de la API.
</p>

![Creación de servicio](/Imagenes/Screenshot_46.png)

<p align="justify">
En caso de que algun contenedor falle, kubernetes se encargara de levantarlo inmediatamente despues de que se detecte el fallo.
</p>

### Conclusion

<p align="justify">
Kubernetes resulta ser una de las mejores opciones en la actualidad para crear sistemas tolerantes a fallos, pues nos permite desplegar multiples replicas de un servicio que se este desplegando y permite una escalabilidad sencilla, aunque la principal ventaja que tiene, en mi opinion, es la de poder levantar los servicios una vez que estos fallaron para que siempre este disponible.
</p>

## Bibliografía

- _¿Qué es Kubernetes?_ (2022, 17 julio). Kubernetes. Recuperado el 24 de Abril de 2023, de https://kubernetes.io/es/docs/concepts/overview/what-is-kubernetes/
- Howtoforge, Howtoforge, & Howtoforge. (2021, 2 junio). _Qué es el Controlador Ingress y cómo desplegar el Controlador Ingress de Nginx en el Cluster Kubernetes en AWS usando Helm_. HowtoForge. Recuperado el 24 de Abril de 2023, de https://howtoforge.es/que-es-el-controlador-ingress-y-como-desplegar-el-controlador-ingress-de-nginx-en-el-cluster-kubernetes-en-aws-usando-helm/
- _¿Qué es un Application Load Balancer? - Elastic Load Balancing_. (s. f.). Recuperado el 24 de Abril de 2023, de https://docs.aws.amazon.com/es_es/elasticloadbalancing/latest/application/introduction.html
