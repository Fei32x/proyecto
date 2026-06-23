# proyecto
Manual de Operaciones del Squad
1. Definition of Done — DoD
Una tarea se considera terminada cuando cumple con los siguientes criterios:
El código está completo y funciona correctamente.
El código pasa la revisión del linter sin errores.
Se ejecutaron pruebas unitarias y/o de integración según corresponda.
La funcionalidad cumple con los requisitos de negocio definidos.
La conexión entre UI, API y Base de Datos fue validada cuando aplica.
La documentación UML se encuentra actualizada.
El Pull Request fue revisado y aprobado por otro integrante del Squad.
La tarea fue movida a la columna “Done” del tablero Kanban.
2. Definition of Ready — DoR
Una historia de usuario o tarea está lista para iniciar cuando cumple con:
Tiene una descripción clara.
Tiene criterios de aceptación definidos.
Está priorizada dentro del Product Backlog.
El equipo entiende qué debe desarrollarse.
No existen dudas importantes sobre el alcance.
Se identificaron los módulos afectados: frontend, backend o base de datos.
Está ubicada en la columna correspondiente del tablero Kanban.
3. Acuerdos de Trabajo del Squad
El Squad trabajará siguiendo estas reglas:
La Daily Scrum se realizará por WhatsApp o Discord.
Cada integrante debe informar qué hizo, qué hará y si tiene algún bloqueo.
El tablero Kanban será actualizado cada vez que una tarea cambie de estado.
Todo cambio importante debe realizarse mediante Pull Request.
Los Pull Requests serán revisados por un compañero antes de fusionarse.
La rama principal será main.
La rama de desarrollo será develop.
Las nuevas funcionalidades se trabajarán en ramas tipo feature/nombre-funcionalidad.
Las correcciones se trabajarán en ramas tipo fix/nombre-error.
4. Flujo de Trabajo en Git
El equipo utilizará el siguiente flujo:
Crear una rama desde develop.
Desarrollar la funcionalidad o corrección.
Realizar commits con mensajes claros.
Subir los cambios al repositorio remoto.
Crear un Pull Request hacia develop.
Solicitar revisión de otro integrante.
Corregir observaciones si existen.
Fusionar el Pull Request cuando esté aprobado.
5. Estándares de Nomenclatura
El Squad utilizará los siguientes estándares:
Variables y funciones: camelCase.
Archivos y carpetas: snake_case o nombres en minúscula.
Clases y componentes: PascalCase.
Ramas de Git:
feature/nombre-funcionalidad
fix/nombre-error
hotfix/nombre-urgente
Commits:
feat: agregar nueva funcionalidad
fix: corregir error
docs: actualizar documentación
test: agregar pruebas
refactor: mejorar código sin cambiar funcionalidad
6. Evidencias del Entregable
El informe debe incluir:
Enlace al repositorio de GitHub con acceso para el docente.
Captura de pantalla de la estructura de ramas.
Captura del tablero Kanban configurado.
Captura del Smoke Test demostrando la conexión exitosa UI → API → DB.
Documento de estándares con DoD, DoR, acuerdos de trabajo y flujo de Git.
