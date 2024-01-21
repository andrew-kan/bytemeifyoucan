import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { bootstrapApplication } from '@angular/platform-browser';
import { GridComponent } from './grid/grid.component';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes)]
};
bootstrapApplication(GridComponent)
