<template>
  <div>
    <h1>Image viewer</h1>
    <p>Project: {{ $route.params.projectId }}</p>
    <p>Image: {{ $route.params.imageId }}</p>
    <p>Здесь позже будет отображение изображения и bounding box'ы.</p>
  </div>
</template>