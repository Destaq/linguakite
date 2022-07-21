<template>
  <div class="overflow-x-auto">
    <table class="table table-fixed table-compact w-full">
      <thead>
        <tr>
          <th></th>
          <th>Word Lemma</th>
          <th class="w-1/3 whitespace-normal">Definition</th>
          <th>Translation</th>
          <th># of Times Seen</th>
          <th>Frequency</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody class="text-center">
        <tr>
          <th>1</th>
          <td>Dog</td>
          <!-- Todo: figure out wrapping -->
          <td class="w-1/3 whitespace-normal">A domesticated carnivorous mammal that typically has a long snout, an
            acute sense of smell, non-retractable claws, and a barking, howling, or whining voice.</td>
          <td>狗</td>
          <td>27</td>
          <td>263</td>
          <td>
            <button class="btn btn-circle btn-outline btn-xs btn-accent">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
      <div class="btn-group justify-center">
        <button class="btn">«</button>
        <button class="btn w-1/3">Page 22</button>
        <button class="btn">»</button>
      </div>
  </div>
</template>

<style>
.table-fixed td,
.table-fixed th {
  padding: 1rem
    /* 16px */
  ;
  vertical-align: middle;
  white-space: normal;
  text-align: center;
}
</style>
