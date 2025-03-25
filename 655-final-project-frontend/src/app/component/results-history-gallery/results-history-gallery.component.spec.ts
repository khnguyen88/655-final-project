import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResultsHistoryGalleryComponent } from './results-history-gallery.component';

describe('ResultsHistoryGalleryComponent', () => {
  let component: ResultsHistoryGalleryComponent;
  let fixture: ComponentFixture<ResultsHistoryGalleryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResultsHistoryGalleryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ResultsHistoryGalleryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
