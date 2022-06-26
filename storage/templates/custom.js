options = {
        success: function(files){
                send_files(files);
        },
        cancel: function(){
        },
        linkType: "preview",
        multiselect: true,
        extensions:['.pdf'],
};
var button = Dropbox.createChooseButton(options);
document.getElementById("dropboxContainer").appendChild(button);

function send_files(files) {
        var subject = "Shared File Links";
        var body = "";
        for(i = 0; i &amp;amp;amp;amp;lt; files.length; i++){
                body += files[i].name + "\n" + files[i].link + "\n\n";
        }
        location.href = 'mailto:coworker@example.com?Subject='+ escape(subject) + '&amp;amp;amp;amp;amp;body='+ escape(body),'200','200';
}