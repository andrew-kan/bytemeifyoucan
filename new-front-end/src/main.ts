import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { HttpClientModule } from '@angular/common/http';
import { MatNativeDateModule } from '@angular/material/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HomePageComponent } from './app/home-page/home-page.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));


bootstrapApplication(HomePageComponent, {
  providers: [
    HttpClientModule,
    BrowserAnimationsModule,
    MatNativeDateModule,
  ]
}).catch(err => console.error(err));