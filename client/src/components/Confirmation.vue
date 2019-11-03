<template>
  <div>
    <b-alert variant="success" show>{{ message }}</b-alert>
  </div>
</template>

<script>
export default {
  name: 'Confirmation',
  props: ['message'],
};
</script>

<style scoped>

</style>
