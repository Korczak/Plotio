export default class Provide {
  private provide: any = {};

  public getProviders() {
    return this.provide;
  }

  public addProvider(provide: any) {
    this.provide = { ...this.provide, ...provide };
  }
}
