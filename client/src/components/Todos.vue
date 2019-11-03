<template>
  <div class="container">
    <div class="col-sm-10">
      <h1>Задачи</h1>
      <confirmation :message="message"
                    v-if='showConfirmation'>
      </confirmation>
      <button type="button"
              id="task-add"
              class="btn btn-success btn-sm align-left d-block"
              v-b-modal.todo-modal>
        Добавить задачу
      </button>

      <table class="table table-dark table-stripped table-hover">

        <thead class="thead-light">
        <tr>
          <th>Uid</th>
          <th>Описание</th>
          <th>Выполнена?</th>
          <th></th>
        </tr>
        </thead>

        <tbody>
        <tr v-for="(todo, index) in todos" :key="index">
          <td class="todo-uid">{{ todo.uid }}</td>
          <td>{{ todo.description }}</td>
          <td>
            <span v-if="todo.is_completed">Выполнено</span>
            <span v-else>Не выполнено</span>
          </td>
          <td>
            <div class="btn-group" role="group">
              <button type="button" class="btn btn-secondary btn-sm">Обновить</button>
              &nbsp;
              <button type="button" class="btn btn-danger btn-sm">X</button>
            </div>
          </td>
        </tr>
        </tbody>

      </table>

      <b-modal ref="addTodoModal"
               id="todo-modal"
               title="Добавить задачу"
               hide-footer> <!-- Теперь у нас должен наконец открываться сам модал. Обратите -->
                <!-- внимание, что у нас в самом определении соответствующего тэга b-modal -->
                <!-- присутствует hide-footer. Это сделано, потому что мы дополнительно -->
                <!-- доопределяем свои кнопки. -->
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-description-group"
                        label="Описание:"
                        label-for="form-description-input">
            <b-form-input id="form-description-input"
                          type="text"
                          v-model="addTodoForm.description"
                          required
                          placeholder="Завести задачу">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-complete-group">
            <b-form-checkbox-group v-model="addTodoForm.is_completed" id="form-checks">
              <b-form-checkbox value="true">Задача выполнена?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-button type="submit" variant="primary">Добавить</b-button>
          <b-button type="reset" variant="danger">Сброс</b-button>
        </b-form>
      </b-modal>
    </div>
  </div>
</template>

<script>
// импортируем библиотеку для работы с http запросами
import axios from 'axios';
import Confirmation from './Confirmation.vue';

const todoListURL = 'http://localhost:5000/api/tasks/';
const todoAddURL = 'http://localhost:5000/api/tasks/';
// const todoAddURL = 'http://localhost:5000/api/add-task/';
// const dataURL = 'http://localhost:5000/api/tasks/';


export default {
  name: 'Todo',
  data() {
    // наш компонент возвращает в шаблон
    return {
      todos: [],
      // определяем объект addTodoForm у которого те же поля, что и в модальном окне
      addTodoForm: {
        description: '',
        // Единственный нюанс состоит в том, что мы сохраняем is_completed как массив, а не булевую
        // переменную. Это связано со спецификой обработки чекбоксов в javascript ❸ (с точки
        // зрения тех, кто разрабатывал стандарт, необходимость в одинокой галке бывает редко).
        // Именно объект addTodoForm используется внутри модала для привязки к модели через
        // v-model.
        is_completed: [],
      },
      message: '',
      showConfirmation: false,
    };
  },
  // вынесли логику после сreated в методы чтобы не загромомждать
  methods: {
    getTodos() {
      axios.get(todoListURL)
        .then((response) => {
          // по сути кладем ответ из даты ответа в todos
          this.todos = response.data.tasks;
        });
    },
    // Так как сброс полей формы нам нужно делать в обоих случаях (и если мы добавляем задачу, и
    // если отменяем), то мы выносим общий код в метод resetForm, в котором мы просто приводим
    // объект addTodoForm к его изначальному состоянию.
    resetForm() {
      this.addTodoForm.description = '';
      this.addTodoForm.is_completed = [];
    },
    onSubmit(event) {
      event.preventDefault(); //  стопаем действ по умолч
      this.$refs.addTodoModal.hide(); // скрываем форму! использовть для скрытия уведомл
      // формируем даннные для отправки на сервер
      const requestData = {
        description: this.addTodoForm.description, // они привязываются к объекту addTodoForm
        is_completed: this.addTodoForm.is_completed[0],
      };
      // отправляем данные и дергаем обратно данные для обновления таблицы
      axios.post(todoAddURL, requestData)
        .then(() => {
          this.getTodos();
          this.message = `Задача "${requestData.description}" добавлена`;
          this.showConfirmation = true;
          setTimeout(() => {
            this.showConfirmation = false;
          }, 3000);
        });
      // приводим значения полей формы в начальное состояние
      this.resetForm();
    },
    onReset(event) {
      event.preventDefault(); // первым делом отменяет действие по умолчанию для этого объекта,
      // потому что мы сначала должны спрятать модальное окно и потом ещё сбросить форму.
      this.$refs.addTodoModal.hide();
      this.resetForm();
    },
  },
  // определяем поведение компонента при загрузке с помощью created
  components: {
    confirmation: Confirmation,
  },
  created() {
    this.getTodos();
  },
};
</script>

<style>
button#task-add {
  margin-top: 20px;
  margin-bottom: 20px;
}
h1, td {
  text-align: left;
}
.todo-uid {
  text-align: right;
}

</style>
