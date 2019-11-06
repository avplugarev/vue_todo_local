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
            <span v-if='todo.is_completed === "false"'>Не выполнено</span>
            <span v-else>Выполнено</span>
          </td>
          <td>
            <div class="btn-group" role="group">
              <button type="button"
                      class="btn btn-secondary btn-sm"
                      v-b-modal.todo-update-modal
                      @click="updateTodo(todo)">
                Обновить
              </button>
              &nbsp;
              <button type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteTodo(todo)">
                X
              </button>
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
            <b-form-checkbox-group>
              <b-form-checkbox
                id="form-checks"
                v-model="addTodoForm.is_completed"
                value='true'
                unchecked-value='false'>
                Задача выполнена?
              </b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-button type="submit" variant="primary">Добавить</b-button>
          <b-button type="reset" variant="danger">Сброс</b-button>
        </b-form>
      </b-modal>

      <b-modal ref="updateTodoModal"
               id="todo-update-modal"
               title="Update"
               hide-footer>
        <b-form @submit="onUpdateSubmit" @reset="onUpdateReset" class="w-100">
          <b-form-group id="form-update-description-group"
                        label="Описание:"
                        label-for="form-update-description-input">
            <b-form-input id="form-update-description-input"
                          type="text"
                          v-model="updateTodoForm.description"
                          required>
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-update-complete-group">
            <b-form-checkbox-group v-model="updateTodoForm.is_completed" id="form-update-checks">
              <b-form-checkbox
                value='true'
                unchecked-value='false'>
                Задача выполнена?
              </b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-button-group>
            <b-button type="submit" variant="primary">Обновить</b-button>
            <b-button type="reset" variant="danger">Сброс</b-button>
          </b-button-group>
        </b-form>
      </b-modal>
    </div>
  </div>
</template>

<script>
// импортируем библиотеку для работы с http запросами
import Confirmation from './Confirmation.vue';

class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ValidationError';
  }
}
export default {
  name: 'Todo',
  data() {
    // наш компонент возвращает в шаблон
    return {
      todos: [],
      // определяем объект addTodoForm у которого те же поля, что и в модальном окне
      addTodoForm: {
        description: '',
        // Именно объект addTodoForm используется внутри модала для привязки к модели через
        // v-model.
        is_completed: 'false',
      },
      // добавили новый объект для формы изменения задачи
      updateTodoForm: {
        uid: 0,
        description: '',
        is_completed: 'false',
        uuid: 0,
      },
      message: '',
      showConfirmation: false,
    };
  },
  // вынесли логику после сreated в методы чтобы не загромомждать
  methods: {
    getUID() {
      if (localStorage.getItem('counter') === null) {
        const newuid = 0;
        localStorage.setItem('counter', newuid);
      } else {
        const uid = localStorage.getItem('counter');
        const newuid = uid * 1 + 1;
        localStorage.setItem('counter', newuid);
      }
    },
    getTodos() {
      const tasks = [];
      let listUid = 0;
      for (let i = 0; i < localStorage.length; i += 1) {
        const key = localStorage.key(i);
        if (key.indexOf('task') !== -1) {
          const savedtask = JSON.parse(localStorage.getItem(key));
          savedtask.uid = listUid;
          listUid += 1;
          tasks.push(savedtask);
        }
      }
      this.todos = tasks;
    },
    // сброс полей формы приводим объект addTodoForm к его изначальному состоянию.
    resetForm() {
      this.addTodoForm.description = '';
      this.addTodoForm.is_completed = 'false';
      this.getTodos();
    },
    resetFormUpdate() {
      this.updateTodoForm.description = '';
      this.updateTodoForm.is_completed = 'false';
      this.getTodos();
    },
    onSubmit(event) {
      event.preventDefault(); //  стопаем действ по умолч
      this.$refs.addTodoModal.hide(); // скрываем форму! использовть для скрытия уведомл
      // формируем даннные для отправки на сервер
      if (this.addTodoForm.is_completed !== 'false') {
        this.addTodoForm.is_completed = 'true';
      }
      this.getUID();
      const mykey = 'task';
      try {
        const savedData = {
          description: this.addTodoForm.description,
          is_completed: this.addTodoForm.is_completed,
          uid: localStorage.getItem('counter'),
          uuid: mykey + localStorage.getItem('counter'),
        };
        const json = JSON.stringify(savedData);
        savedData.uuid = mykey + savedData.uid;
        localStorage.setItem(savedData.uuid, json);
        this.message = 'Задача добавлена в список';
      } catch (e) {
        console.log(e);
        this.message = 'Произошла ошибка. Задача не добавлена в список';
      }
      // приводим значения полей формы в начальное состояние
      this.resetForm();
      this.getTodos();
      this.showConfirmation = true;
      setTimeout(() => {
        this.showConfirmation = false;
      }, 5000);
    },
    onReset(event) {
      event.preventDefault(); // первым делом отменяет действие по умолчанию для этого объекта,
      // потому что мы сначала должны спрятать модальное окно и потом ещё сбросить форму.
      this.$refs.addTodoModal.hide();
      this.resetForm();
    },
    // обновляем объект с обновлен данныммы в новом методе updateTodo
    updateTodo(todo) {
      this.updateTodoForm = todo;
    },
    onUpdateSubmit(event) {
      // делаем тоже самое что с сабмит просто другим методом
      event.preventDefault();
      this.$refs.updateTodoModal.hide();
      if (this.addTodoForm.is_completed !== 'false') {
        this.addTodoForm.is_completed = 'true';
      }
      try {
        if (localStorage.getItem(this.updateTodoForm.uuid) === null) {
          throw new ValidationError();
        }
        const savedData = {
          description: this.updateTodoForm.description,
          is_completed: this.updateTodoForm.is_completed,
          uid: this.updateTodoForm.uid,
          uuid: this.updateTodoForm.uuid,
        };
        const json = JSON.stringify(savedData);
        localStorage.setItem(savedData.uuid, json);
        this.message = 'Задача обновлена';
      } catch (e) {
        if (e instanceof ValidationError) {
          console.log(e.name);
          this.message = 'Произошла ошибка. Задача с таким номером отсутствует';
        } else {
          console.log(e);
          this.message = 'Произошла ошибка во время обновления задачи';
        }
      }
      this.resetFormUpdate();
      this.getTodos();
      this.showConfirmation = true;
      setTimeout(() => {
        this.showConfirmation = false;
      }, 5000);
    },
    onUpdateReset(event) {
      event.preventDefault();
      this.$refs.updateTodoModal.hide();
      this.resetFormUpdate();
    },
    deleteTodo(todo) {
      try {
        const toDeleteUuid = todo.uuid;
        if (localStorage.getItem(toDeleteUuid) === null) {
          throw new ValidationError();
        }
        localStorage.removeItem(toDeleteUuid);
        this.message = 'Задача удалена из списка';
      } catch (e) {
        if (e instanceof ValidationError) {
          console.log(e.name);
          this.message = 'Произошла ошибка. Задача с таким номером отсутствует}';
        } else {
          console.log(e);
          this.message = 'Произошла ошибка во время удаления задачи';
        }
      }
      this.getTodos();
      this.showConfirmation = true;
      setTimeout(() => {
        this.showConfirmation = false;
      }, 5000);
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
