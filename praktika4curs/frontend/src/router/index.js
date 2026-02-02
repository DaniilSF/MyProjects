import { createRouter, createWebHistory } from "vue-router";

import ProjectsPage from "../pages/ProjectsPage.vue";
import ProjectImagesPage from "../pages/ProjectImagesPage.vue";
import ImageViewerPage from "../pages/ImageViewerPage.vue";

const routes = [
  { path: "/", redirect: "/projects" },
  { path: "/projects", component: ProjectsPage },
  { path: "/projects/:projectId", component: ProjectImagesPage },
  { path: "/projects/:projectId/images/:imageId", component: ImageViewerPage },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});