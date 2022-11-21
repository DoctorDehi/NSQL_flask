function wordMap() {
    var words = this.text.match(/\w+/g);

    if (words == null) {
        return;
    }

    for (var i = 0; i < words.length; i++) {
        emit(words[i], {count: 1});
    }
}

function wordReduce(key, values) {
    var total = 0;
    for (var i = 0; i < values.length; i++) {
        total += values[i].count;
    }

    return {count: total};
}