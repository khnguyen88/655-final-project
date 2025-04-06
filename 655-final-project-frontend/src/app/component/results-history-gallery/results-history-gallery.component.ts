import { Component, ChangeDetectionStrategy, ChangeDetectorRef, OnDestroy, OnInit } from '@angular/core';
import { ImagesService } from '../../service/images.service';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-results-history-gallery',
  templateUrl: './results-history-gallery.component.html',
  styleUrl: './results-history-gallery.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: true,
  imports: [],
})
  
export class ResultsHistoryGalleryComponent implements OnInit, OnDestroy{
  subscriptions: Subscription = new Subscription();

  imageRequestHistoryData: any;

  constructor(private imageService: ImagesService, private router: Router, private cd: ChangeDetectorRef) {
    
  }

  ngOnInit(): void {
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;

    this.subscriptions.add(this.imageService.getSearchResultsHistory().subscribe(
      results => {
        this.imageRequestHistoryData = results;
        alert(JSON.stringify(this.imageRequestHistoryData));
        this.cd.detectChanges();
      }
    ));
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

}
