<div class="background-decoration"></div>
<div class="clouds"></div>

<style>
    .background-decoration {
        position: fixed;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        background-image:
                radial-gradient(circle at 80% 20%, #ffffff33 1%, transparent 10%),
                radial-gradient(circle at 20% 80%, #ffffff33 1%, transparent 10%),
                radial-gradient(circle at 50% 50%, #ffffff33 1%, transparent 10%),
                radial-gradient(circle at 10% 10%, #ffffff33 1%, transparent 10%),
                radial-gradient(circle at 90% 90%, #ffffff33 1%, transparent 10%);
    }

    .clouds {
        position: fixed;
        width: 100%;
        height: 100%;
        background:
                url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"><path d="M20,50 Q30,40 40,50 Q50,40 60,50 Q70,40 80,50 Q90,40 100,50" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"/></svg>') repeat-x;
        animation: floatClouds 30s linear infinite;
        pointer-events: none;
    }

    @keyframes floatClouds {
        from { background-position: 0 0; }
        to { background-position: 1000px 0; }
    }
</style>