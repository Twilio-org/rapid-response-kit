(function(window, $) {
    // Rapid Response Kit namespace
    var rrk = window.rrk = {};

    // Listen for the jQuery ready event on the document
    $(function() {
        $.extend(rrk, {
            setLanguages: function(voices) {
                var $voiceEngine = $("#voice-engine"),
                    $voiceLanguage = $("#voice-language"),
                    s = '<select id="voice-language" name="voice-language" class="form-control">',
                    selectedEngine = $voiceEngine.val(),
                    selected = "";

                for (var i = 0, l = voices[selectedEngine].length; i < l; i++) {
                    selected = (voices[selectedEngine][i].
                        default === true) ? "selected " : "";
                    s += "<option " + selected + "value=\"" + voices[selectedEngine][i].value + "\">" + voices[selectedEngine][i].name + "</option>";
                }

                s += "</select>";

                $voiceLanguage.replaceWith(s);
            }
        });
    });
}(window, window.jQuery));
