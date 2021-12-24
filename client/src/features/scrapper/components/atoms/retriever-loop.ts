import { Component, Mixins, Prop, Vue } from "vue-property-decorator";

@Component({})
export default class RetrieverLoop extends Vue {
  retrieve_working: boolean = true;

  delay(milliseconds: number) {
    return new Promise((resolve) => {
      setTimeout(resolve, milliseconds);
    });
  }

  async retrieve_loop(retriever_function: any, delayMs: number = 1000) {
    while (this.retrieve_working) {
      await retriever_function();
      await this.delay(1000);
    }
  }
}
