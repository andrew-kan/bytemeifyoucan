import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportantTilesComponent } from './important-tiles.component';

describe('ImportantTilesComponent', () => {
  let component: ImportantTilesComponent;
  let fixture: ComponentFixture<ImportantTilesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImportantTilesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ImportantTilesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
