<template>
  <div>
    <b-alert show dismissible variant='success'>{{ message }}</b-alert>
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
