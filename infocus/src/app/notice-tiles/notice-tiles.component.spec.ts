import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NoticeTilesComponent } from './notice-tiles.component';

describe('NoticeTilesComponent', () => {
  let component: NoticeTilesComponent;
  let fixture: ComponentFixture<NoticeTilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NoticeTilesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(NoticeTilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
